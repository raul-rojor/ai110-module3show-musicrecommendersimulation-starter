import csv
import heapq
from operator import itemgetter
from typing import Any, Dict, Iterable, List, Tuple, Union
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

# ---------------------------------------------------------------------------
# Algorithm Recipe (Phase 2): content-based scoring
# ---------------------------------------------------------------------------
# Every feature yields a 0-1 sub-score. Qualitative features (genre, mood) use
# any-match against the user's list of accepted values; quantitative features
# score by *closeness* to the user's target, so a song is judged relative to
# what the user wants rather than "higher is better". `artist` is excluded.
#
# Weights follow the agreed importance order: genre is bumped above a linear
# split, and the remaining six are linearly aligned amongst themselves
# (6:5:4:3:2:1). Any feature the profile omits is dropped and the remaining
# weights are renormalized, so the final score always lands in [0, 1].
WEIGHTS: Dict[str, float] = {
    "genre":        0.300,
    "acousticness": 0.200,
    "energy":       0.167,
    "mood":         0.133,
    "danceability": 0.100,
    "valence":      0.067,
    "tempo_bpm":    0.033,
}
QUALITATIVE_FEATURES = frozenset({"genre", "mood"})

# Tempo is the only feature not already on a 0-1 scale, so it is min-max
# normalized against these bounds before the closeness formula is applied.
TEMPO_MIN, TEMPO_MAX = 40.0, 220.0
TEMPO_SPAN = TEMPO_MAX - TEMPO_MIN


def _clamp01(x: float) -> float:
    """Clamp a value into the [0, 1] range."""
    return 0.0 if x < 0.0 else 1.0 if x > 1.0 else x


def _normalize_tempo(bpm: float) -> float:
    """Map a raw BPM onto a 0-1 scale using the fixed tempo bounds."""
    return _clamp01((float(bpm) - TEMPO_MIN) / TEMPO_SPAN)


def _value(song: Union[Dict, "Song"], feature: str) -> Any:
    """Read a feature from either a dict (functional path) or a Song object."""
    return song[feature] if isinstance(song, dict) else getattr(song, feature)


def _has_preference(target: Any) -> bool:
    """True if the profile expresses a usable preference for this feature."""
    if target is None or target == "":
        return False
    if isinstance(target, (list, tuple, set, frozenset)) and not target:
        return False
    return True


def _feature_subscore(feature: str, target: Any, value: Any) -> float:
    """Score a single feature in [0, 1], relative to the user's preference."""
    if feature in QUALITATIVE_FEATURES:
        options = target if isinstance(target, (list, tuple, set, frozenset)) else (target,)
        return 1.0 if value in options else 0.0
    if feature == "tempo_bpm":
        return 1.0 - abs(_normalize_tempo(value) - _normalize_tempo(target))
    return _clamp01(1.0 - abs(float(value) - float(target)))


def _reason(feature: str, target: Any, value: Any, sub: float, share: float) -> str:
    """Human-readable, inspectable note on one feature's contribution."""
    contribution = share * sub
    if feature in QUALITATIVE_FEATURES:
        verdict = "matches" if sub else "not in"
        return f"{feature} '{value}' {verdict} your preferences (+{contribution:.2f})"
    return f"{feature} {value} vs target {target} (match {sub:.0%}, +{contribution:.2f})"


def _score_core(prefs: Dict[str, Any], song: Union[Dict, "Song"]) -> Tuple[float, List[str]]:
    """Shared engine scoring a song against a prefs dict -> (score in [0,1], reasons)."""
    active: List[Tuple[str, Any, Any, float, float]] = []
    total_weight = 0.0
    # Iterate WEIGHTS (importance order) so reasons are always ordered the same.
    for feature, weight in WEIGHTS.items():
        target = prefs.get(feature)
        if not _has_preference(target):
            continue
        sub = _feature_subscore(feature, target, _value(song, feature))
        active.append((feature, target, _value(song, feature), sub, weight))
        total_weight += weight

    if not total_weight:
        return 0.0, []

    score = sum(weight * sub for *_, sub, weight in active) / total_weight
    reasons = [_reason(f, t, v, sub, weight / total_weight) for f, t, v, sub, weight in active]
    return score, reasons


def _profile_to_prefs(user: "UserProfile") -> Dict[str, Any]:
    """Adapt a dataclass UserProfile into the dict prefs format the engine expects."""
    return {
        "genre": [user.favorite_genre],
        "mood": [user.favorite_mood],
        "energy": user.target_energy,
        "acousticness": 1.0 if user.likes_acoustic else 0.0,
    }


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        prefs = _profile_to_prefs(user)
        return heapq.nlargest(k, self.songs, key=lambda song: _score_core(prefs, song)[0])

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        prefs = _profile_to_prefs(user)
        score, reasons = _score_core(prefs, song)
        detail = "; ".join(reasons) if reasons else "no matching preferences"
        return f"Score {score:.2f} — {detail}"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file into a list of dictionaries.
    Required by src/main.py

    Numeric columns are converted from strings to the correct types:
    - `id` becomes an int
    - `energy`, `tempo_bpm`, `valence`, `danceability`, `acousticness` become floats
    The remaining columns (title, artist, genre, mood) stay as strings.
    """
    int_columns = ("id",)
    float_columns = ("energy", "tempo_bpm", "valence", "danceability", "acousticness")

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            song = dict(row)
            for col in int_columns:
                song[col] = int(song[col])
            for col in float_columns:
                song[col] = float(song[col])
            songs.append(song)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences using the Algorithm Recipe.
    Required by recommend_songs() and src/main.py

    `user_prefs` is a dict of feature -> preference:
    - genre / mood: a list of accepted values (a bare string is also accepted)
    - acousticness / energy / danceability / valence: a numeric target in [0, 1]
    - tempo_bpm: a target in raw BPM
    Omitted features are ignored. Returns (score in [0, 1], reasons).
    """
    return _score_core(user_prefs, song)


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Scores every song, then returns the top-k as (song, score, explanation),
    ranked by score (highest first).
    Required by src/main.py
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons) if reasons else "no matching preferences"
        scored.append((song, score, explanation))
    return heapq.nlargest(k, scored, key=itemgetter(1))
