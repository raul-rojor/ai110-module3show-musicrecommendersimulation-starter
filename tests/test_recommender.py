from src.recommender import (
    Song,
    UserProfile,
    Recommender,
    score_song,
    recommend_songs,
    load_songs,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def make_song(**overrides) -> dict:
    """A neutral song dict; override any field for a specific case."""
    base = dict(
        id=1, title="T", artist="A", genre="pop", mood="happy",
        energy=0.5, tempo_bpm=120.0, valence=0.5, danceability=0.5, acousticness=0.5,
    )
    base.update(overrides)
    return base


def make_song_obj(**overrides) -> Song:
    return Song(**make_song(**overrides))


def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


# ---------------------------------------------------------------------------
# Existing behaviour (kept)
# ---------------------------------------------------------------------------
def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


# ---------------------------------------------------------------------------
# score_song: output contract & score bounds
# ---------------------------------------------------------------------------
def test_score_song_returns_score_and_reasons():
    score, reasons = score_song({"genre": ["pop"]}, make_song())
    assert isinstance(score, float)
    assert isinstance(reasons, list)
    assert all(isinstance(r, str) for r in reasons)


def test_score_always_within_unit_interval():
    prefs = {
        "genre": ["pop", "lofi"], "mood": ["happy"], "acousticness": 0.1,
        "energy": 0.9, "danceability": 0.7, "valence": 0.8, "tempo_bpm": 200,
    }
    songs = [
        make_song(genre="pop", energy=0.9, tempo_bpm=200),          # near-perfect
        make_song(genre="metal", mood="sad", energy=0.05, tempo_bpm=40, acousticness=1.0),  # far
        make_song(),                                                 # neutral
    ]
    for song in songs:
        score, _ = score_song(prefs, song)
        assert 0.0 <= score <= 1.0


def test_empty_preferences_scores_zero():
    score, reasons = score_song({}, make_song())
    assert score == 0.0
    assert reasons == []


# ---------------------------------------------------------------------------
# Qualitative features: any-match against a list (or bare string)
# ---------------------------------------------------------------------------
def test_qualitative_exact_match_and_mismatch():
    assert score_song({"genre": ["pop"]}, make_song(genre="pop"))[0] == 1.0
    assert score_song({"genre": ["pop"]}, make_song(genre="rock"))[0] == 0.0


def test_qualitative_list_matches_any_listed_value():
    prefs = {"genre": ["rock", "pop", "jazz"]}
    assert score_song(prefs, make_song(genre="jazz"))[0] == 1.0
    assert score_song(prefs, make_song(genre="metal"))[0] == 0.0


def test_bare_string_preference_equals_single_item_list():
    song = make_song(genre="pop")
    assert score_song({"genre": "pop"}, song)[0] == score_song({"genre": ["pop"]}, song)[0]


# ---------------------------------------------------------------------------
# Quantitative features: closeness, relative to preference (not higher-is-better)
# ---------------------------------------------------------------------------
def test_numeric_scoring_is_relative_to_target():
    # A user who wants LOW energy should prefer the low-energy song.
    prefs = {"energy": 0.2}
    low = score_song(prefs, make_song(energy=0.2))[0]
    high = score_song(prefs, make_song(energy=0.9))[0]
    assert low == 1.0
    assert low > high


def test_tempo_is_normalized_before_closeness():
    prefs = {"tempo_bpm": 120}
    on_target = score_song(prefs, make_song(tempo_bpm=120))[0]
    far_off = score_song(prefs, make_song(tempo_bpm=40))[0]
    assert on_target == 1.0
    assert on_target > far_off > 0.0


# ---------------------------------------------------------------------------
# Missing features are dropped and remaining weights renormalized
# ---------------------------------------------------------------------------
def test_missing_features_are_renormalized_away():
    prefs = {"genre": ["pop"], "energy": 0.5}  # only 2 of 7 features
    score, reasons = score_song(prefs, make_song(genre="pop", energy=0.5))
    assert len(reasons) == 2          # only the supplied features are scored
    assert score == 1.0               # both match perfectly -> full score despite omissions


def test_partial_match_stays_bounded():
    prefs = {"genre": ["pop"], "energy": 0.5}
    better = score_song(prefs, make_song(genre="pop", energy=0.5))[0]
    worse = score_song(prefs, make_song(genre="pop", energy=1.0))[0]
    assert 0.0 <= worse < better <= 1.0


# ---------------------------------------------------------------------------
# recommend_songs: ranking and k bounds
# ---------------------------------------------------------------------------
def test_recommend_songs_ranks_by_score_descending():
    prefs = {"genre": ["pop"], "mood": ["happy"], "energy": 0.8}
    songs = [
        make_song(id=1, genre="pop", mood="happy", energy=0.8),   # best
        make_song(id=2, genre="pop", mood="happy", energy=0.4),   # mood/genre ok, energy off
        make_song(id=3, genre="rock", mood="sad", energy=0.1),    # worst
    ]
    ranked = recommend_songs(prefs, songs, k=3)
    scores = [score for _, score, _ in ranked]
    assert [s["id"] for s, _, _ in ranked] == [1, 2, 3]
    assert scores == sorted(scores, reverse=True)


def test_recommend_songs_respects_k():
    prefs = {"genre": ["pop"]}
    songs = [make_song(id=i) for i in range(5)]
    assert len(recommend_songs(prefs, songs, k=2)) == 2


def test_recommend_songs_k_larger_than_catalog():
    prefs = {"genre": ["pop"]}
    songs = [make_song(id=1), make_song(id=2)]
    assert len(recommend_songs(prefs, songs, k=10)) == 2


def test_recommend_songs_empty_catalog():
    assert recommend_songs({"genre": ["pop"]}, [], k=5) == []


def test_recommend_songs_k_zero():
    assert recommend_songs({"genre": ["pop"]}, [make_song()], k=0) == []


def test_recommend_songs_returns_explanation_string():
    ranked = recommend_songs({"genre": ["pop"]}, [make_song(genre="pop")], k=1)
    _, _, explanation = ranked[0]
    assert isinstance(explanation, str) and explanation.strip() != ""


# ---------------------------------------------------------------------------
# OOP Recommender: edge cases
# ---------------------------------------------------------------------------
def test_recommend_empty_catalog_returns_empty():
    rec = Recommender([])
    user = UserProfile("pop", "happy", 0.8, False)
    assert rec.recommend(user, k=3) == []


def test_recommend_k_larger_than_catalog_returns_all():
    rec = make_small_recommender()
    user = UserProfile("pop", "happy", 0.8, False)
    assert len(rec.recommend(user, k=99)) == 2


def test_likes_acoustic_flips_preference_direction():
    acoustic = make_song_obj(id=1, acousticness=0.9)
    electronic = make_song_obj(id=2, acousticness=0.1)
    rec = Recommender([acoustic, electronic])

    likes = UserProfile("pop", "happy", 0.5, likes_acoustic=True)
    dislikes = UserProfile("pop", "happy", 0.5, likes_acoustic=False)

    assert rec.recommend(likes, k=1)[0].id == 1        # prefers the acoustic track
    assert rec.recommend(dislikes, k=1)[0].id == 2     # prefers the electronic track


def test_explain_recommendation_reports_score():
    rec = make_small_recommender()
    user = UserProfile("pop", "happy", 0.8, False)
    explanation = rec.explain_recommendation(user, rec.songs[0])
    assert "Score" in explanation


# ---------------------------------------------------------------------------
# load_songs: parsing & type conversion (isolated temp file)
# ---------------------------------------------------------------------------
def test_load_songs_parses_rows_and_types(tmp_path):
    csv_path = tmp_path / "songs.csv"
    csv_path.write_text(
        "id,title,artist,genre,mood,energy,tempo_bpm,valence,danceability,acousticness\n"
        "1,A Song,An Artist,pop,happy,0.8,120,0.7,0.6,0.2\n"
        "2,B Song,An Artist,lofi,chill,0.4,80,0.5,0.5,0.9\n"
    )
    songs = load_songs(str(csv_path))

    assert len(songs) == 2
    first = songs[0]
    assert isinstance(first["id"], int) and first["id"] == 1
    for col in ("energy", "tempo_bpm", "valence", "danceability", "acousticness"):
        assert isinstance(first[col], float)
    for col in ("title", "artist", "genre", "mood"):
        assert isinstance(first[col], str)


def test_load_songs_empty_file_returns_empty(tmp_path):
    csv_path = tmp_path / "empty.csv"
    csv_path.write_text(
        "id,title,artist,genre,mood,energy,tempo_bpm,valence,danceability,acousticness\n"
    )
    assert load_songs(str(csv_path)) == []
