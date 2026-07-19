# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

Streaming platforms combine content-based and collaborative filtering in order to recommend media to users. Collaborative filtering recommends media based on similar users' liked content which the user hasn't viewed yet, while content-based filtering recommends media based on content matching the user's past content preferences. My recommendation model uses content-based filtering since a user database which allows mutliple users to be stored and compared is not included. Each song in my system and user profile has genre, acousticness, energt, mood, danceability, valence, and tempo features to be used for song scoring relative to users. The recommender computes target feature values based on the user's preferences and then scores the closeness of songs' features to the target values. Then, weights are applied to the normalized closeness scores based on feature importance and are then added. Finally, the songs with the highest scores are recommended first to the user.

THe user profile will include a dictionary of preferences where 'genre' and 'mood' have list values and the other song qualities have numerical values. Weights for song feature importance are the following:
genre	0.300
acousticness	0.200
energy	0.167
mood	0.133
danceability	0.100
valence	0.067
tempo_bpm	0.033.

Scoring of song features is done relative to user preferences, where the absolute value of the difference between the song's feature score and the user's preferred feature score is subtracted from 1 and that value is multiplied by the feature's weight. A song's genre and mood are scored for a user as either a 1.00 or 0.00 since the variable is discrete. The scoring of tempo bpm begins with normalizing tempo bpm values of the song and the user preferences from the 40 - 220 domain. The high weight of acousticness may be excessive and lead to a bias for acousticness matches in songs, but I believe that the variable makes a very impactful difference in songs and therefore should be heavily weighted. Still, adjustments may be clearly necessary after testing. Additionally, the care I personally have for the various aspects of music likely caused biases in my weighing of song features.

The recommender will use two primary functions in it's logic: score_song(user_prefs: dict, song: dict) -> (score, reasons) and recommend_songs(user_prefs, songs, k) -> list[(song, score, explanation)]. The reasons and explanations outputted by these functions do not reflect the outputs of real recommendation algorithms of streaming services, especially since their scores are not readable. Instead, the reason for these outputs in this simulation is so that score outputs can be used by the developer to understand the scoring logic and subsequently enact changes.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
==============================================================
  🎵  Top Music Recommendations
  for  genre=pop · mood=happy · energy=0.8
==============================================================

  1. Sunrise City — Neon Echo                  ██████████ 0.99
        ├─ genre 'pop' matches your preferences (+0.50)
        ├─ energy 0.82 vs target 0.8 (match 98%, +0.27)
        └─ mood 'happy' matches your preferences (+0.22)

  2. Gym Hero — Max Pulse                      ███████░░░ 0.74
        ├─ genre 'pop' matches your preferences (+0.50)
        ├─ energy 0.93 vs target 0.8 (match 87%, +0.24)
        └─ mood 'intense' not in your preferences (+0.00)

  3. Rooftop Lights — Indigo Parade            █████░░░░░ 0.49
        ├─ genre 'indie pop' not in your preferences (+0.00)
        ├─ energy 0.76 vs target 0.8 (match 96%, +0.27)
        └─ mood 'happy' matches your preferences (+0.22)

  4. Disco Fever Dream — Glitter Avenue        ███░░░░░░░ 0.28
        ├─ genre 'disco' not in your preferences (+0.00)
        ├─ energy 0.8 vs target 0.8 (match 100%, +0.28)
        └─ mood 'playful' not in your preferences (+0.00)

  5. Concrete Bars — Rhyme Theory              ███░░░░░░░ 0.27
        ├─ genre 'hip-hop' not in your preferences (+0.00)
        ├─ energy 0.76 vs target 0.8 (match 96%, +0.27)
        └─ mood 'confident' not in your preferences (+0.00)

==============================================================
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

## Profile Evaluation

Top-5 recommendations from `python -m src.main` for three normal listener personas and three adversarial / edge-case profiles.

### High-Energy Pop

`{'genre': ['pop'], 'mood': ['happy', 'uplifting'], 'energy': 0.9, 'danceability': 0.85, 'valence': 0.85}`

```
==============================================================
  🎵  Top Music Recommendations
  for  genre=pop · mood=happy, uplifting · energy=0.9 · danceability=0.85 · valence=0.85
==============================================================

  1. Sunrise City — Neon Echo                  ██████████ 0.97
        ├─ genre 'pop' matches your preferences (+0.39)
        ├─ energy 0.82 vs target 0.9 (match 92%, +0.20)
        ├─ mood 'happy' matches your preferences (+0.17)
        ├─ danceability 0.79 vs target 0.85 (match 94%, +0.12)
        └─ valence 0.84 vs target 0.85 (match 99%, +0.09)

  2. Gym Hero — Max Pulse                      ████████░░ 0.81
        ├─ genre 'pop' matches your preferences (+0.39)
        ├─ energy 0.93 vs target 0.9 (match 97%, +0.21)
        ├─ mood 'intense' not in your preferences (+0.00)
        ├─ danceability 0.88 vs target 0.85 (match 97%, +0.13)
        └─ valence 0.77 vs target 0.85 (match 92%, +0.08)

  3. Rooftop Lights — Indigo Parade            ██████░░░░ 0.57
        ├─ genre 'indie pop' not in your preferences (+0.00)
        ├─ energy 0.76 vs target 0.9 (match 86%, +0.19)
        ├─ mood 'happy' matches your preferences (+0.17)
        ├─ danceability 0.82 vs target 0.85 (match 97%, +0.13)
        └─ valence 0.81 vs target 0.85 (match 96%, +0.08)

  4. Island Time — Palm and Bass               █████░░░░░ 0.54
        ├─ genre 'reggae' not in your preferences (+0.00)
        ├─ energy 0.6 vs target 0.9 (match 70%, +0.15)
        ├─ mood 'uplifting' matches your preferences (+0.17)
        ├─ danceability 0.83 vs target 0.85 (match 98%, +0.13)
        └─ valence 0.86 vs target 0.85 (match 99%, +0.09)

  5. Pulse Reactor — Voltage Kids              ████░░░░░░ 0.41
        ├─ genre 'techno' not in your preferences (+0.00)
        ├─ energy 0.95 vs target 0.9 (match 95%, +0.21)
        ├─ mood 'euphoric' not in your preferences (+0.00)
        ├─ danceability 0.9 vs target 0.85 (match 95%, +0.12)
        └─ valence 0.74 vs target 0.85 (match 89%, +0.08)

==============================================================
```

### Chill Lofi

`{'genre': ['lofi', 'ambient'], 'mood': ['chill', 'relaxed', 'focused'], 'energy': 0.35, 'acousticness': 0.8, 'tempo_bpm': 75}`

```
==============================================================
  🎵  Top Music Recommendations
  for  genre=lofi, ambient · mood=chill, relaxed, focused · energy=0.35 · acousticness=0.8 · tempo_bpm=75
==============================================================

  1. Library Rain — Paper Lanterns             ██████████ 0.98
        ├─ genre 'lofi' matches your preferences (+0.36)
        ├─ acousticness 0.86 vs target 0.8 (match 94%, +0.23)
        ├─ energy 0.35 vs target 0.35 (match 100%, +0.20)
        ├─ mood 'chill' matches your preferences (+0.16)
        └─ tempo_bpm 72.0 vs target 75 (match 98%, +0.04)

  2. Focus Flow — LoRoom                       ██████████ 0.98
        ├─ genre 'lofi' matches your preferences (+0.36)
        ├─ acousticness 0.78 vs target 0.8 (match 98%, +0.24)
        ├─ energy 0.4 vs target 0.35 (match 95%, +0.19)
        ├─ mood 'focused' matches your preferences (+0.16)
        └─ tempo_bpm 80.0 vs target 75 (match 97%, +0.04)

  3. Midnight Coding — LoRoom                  ██████████ 0.96
        ├─ genre 'lofi' matches your preferences (+0.36)
        ├─ acousticness 0.71 vs target 0.8 (match 91%, +0.22)
        ├─ energy 0.42 vs target 0.35 (match 93%, +0.19)
        ├─ mood 'chill' matches your preferences (+0.16)
        └─ tempo_bpm 78.0 vs target 75 (match 98%, +0.04)

  4. Spacewalk Thoughts — Orbit Bloom          ██████████ 0.95
        ├─ genre 'ambient' matches your preferences (+0.36)
        ├─ acousticness 0.92 vs target 0.8 (match 88%, +0.21)
        ├─ energy 0.28 vs target 0.35 (match 93%, +0.19)
        ├─ mood 'chill' matches your preferences (+0.16)
        └─ tempo_bpm 60.0 vs target 75 (match 92%, +0.04)

  5. Coffee Shop Stories — Slow Stereo         ██████░░░░ 0.61
        ├─ genre 'jazz' not in your preferences (+0.00)
        ├─ acousticness 0.89 vs target 0.8 (match 91%, +0.22)
        ├─ energy 0.37 vs target 0.35 (match 98%, +0.20)
        ├─ mood 'relaxed' matches your preferences (+0.16)
        └─ tempo_bpm 90.0 vs target 75 (match 92%, +0.04)

==============================================================
```

### Deep Intense Rock

`{'genre': ['rock', 'metal'], 'mood': ['intense', 'aggressive'], 'energy': 0.92, 'acousticness': 0.05, 'tempo_bpm': 150}`

```
==============================================================
  🎵  Top Music Recommendations
  for  genre=rock, metal · mood=intense, aggressive · energy=0.92 · acousticness=0.05 · tempo_bpm=150
==============================================================

  1. Storm Runner — Voltline                   ██████████ 0.99
        ├─ genre 'rock' matches your preferences (+0.36)
        ├─ acousticness 0.1 vs target 0.05 (match 95%, +0.23)
        ├─ energy 0.91 vs target 0.92 (match 99%, +0.20)
        ├─ mood 'intense' matches your preferences (+0.16)
        └─ tempo_bpm 152.0 vs target 150 (match 99%, +0.04)

  2. Iron Verdict — Ashen Crown                ██████████ 0.98
        ├─ genre 'metal' matches your preferences (+0.36)
        ├─ acousticness 0.03 vs target 0.05 (match 98%, +0.24)
        ├─ energy 0.97 vs target 0.92 (match 95%, +0.19)
        ├─ mood 'aggressive' matches your preferences (+0.16)
        └─ tempo_bpm 172.0 vs target 150 (match 88%, +0.03)

  3. Gym Hero — Max Pulse                      ██████░░░░ 0.63
        ├─ genre 'pop' not in your preferences (+0.00)
        ├─ acousticness 0.05 vs target 0.05 (match 100%, +0.24)
        ├─ energy 0.93 vs target 0.92 (match 99%, +0.20)
        ├─ mood 'intense' matches your preferences (+0.16)
        └─ tempo_bpm 132.0 vs target 150 (match 90%, +0.04)

  4. Pulse Reactor — Voltage Kids              █████░░░░░ 0.47
        ├─ genre 'techno' not in your preferences (+0.00)
        ├─ acousticness 0.04 vs target 0.05 (match 99%, +0.24)
        ├─ energy 0.95 vs target 0.92 (match 97%, +0.19)
        ├─ mood 'euphoric' not in your preferences (+0.00)
        └─ tempo_bpm 128.0 vs target 150 (match 88%, +0.03)

  5. Disco Fever Dream — Glitter Avenue        ████░░░░░░ 0.43
        ├─ genre 'disco' not in your preferences (+0.00)
        ├─ acousticness 0.12 vs target 0.05 (match 93%, +0.22)
        ├─ energy 0.8 vs target 0.92 (match 88%, +0.18)
        ├─ mood 'playful' not in your preferences (+0.00)
        └─ tempo_bpm 120.0 vs target 150 (match 83%, +0.03)

==============================================================
```

### Adversarial: Conflicting Signals (high energy + sad mood)

`{'genre': ['rock', 'pop'], 'mood': ['sad'], 'energy': 0.95, 'danceability': 0.9}`

```
==============================================================
  🎵  Top Music Recommendations
  for  genre=rock, pop · mood=sad · energy=0.95 · danceability=0.9
==============================================================

  1. Gym Hero — Max Pulse                      ████████░░ 0.80
        ├─ genre 'pop' matches your preferences (+0.43)
        ├─ energy 0.93 vs target 0.95 (match 98%, +0.23)
        ├─ mood 'intense' not in your preferences (+0.00)
        └─ danceability 0.88 vs target 0.9 (match 98%, +0.14)

  2. Storm Runner — Voltline                   ████████░░ 0.77
        ├─ genre 'rock' matches your preferences (+0.43)
        ├─ energy 0.91 vs target 0.95 (match 96%, +0.23)
        ├─ mood 'intense' not in your preferences (+0.00)
        └─ danceability 0.66 vs target 0.9 (match 76%, +0.11)

  3. Sunrise City — Neon Echo                  ████████░░ 0.76
        ├─ genre 'pop' matches your preferences (+0.43)
        ├─ energy 0.82 vs target 0.95 (match 87%, +0.21)
        ├─ mood 'happy' not in your preferences (+0.00)
        └─ danceability 0.79 vs target 0.9 (match 89%, +0.13)

  4. Rainy Delta — Muddy Fret                  ████░░░░░░ 0.39
        ├─ genre 'blues' not in your preferences (+0.00)
        ├─ energy 0.44 vs target 0.95 (match 49%, +0.12)
        ├─ mood 'sad' matches your preferences (+0.19)
        └─ danceability 0.5 vs target 0.9 (match 60%, +0.09)

  5. Pulse Reactor — Voltage Kids              ████░░░░░░ 0.38
        ├─ genre 'techno' not in your preferences (+0.00)
        ├─ energy 0.95 vs target 0.95 (match 100%, +0.24)
        ├─ mood 'euphoric' not in your preferences (+0.00)
        └─ danceability 0.9 vs target 0.9 (match 100%, +0.14)

==============================================================
```

### Adversarial: Empty Profile (no preferences)

`{}`

```
==============================================================
  🎵  Top Music Recommendations
  for  
==============================================================

  1. Sunrise City — Neon Echo                  ░░░░░░░░░░ 0.00

  2. Midnight Coding — LoRoom                  ░░░░░░░░░░ 0.00

  3. Storm Runner — Voltline                   ░░░░░░░░░░ 0.00

  4. Library Rain — Paper Lanterns             ░░░░░░░░░░ 0.00

  5. Gym Hero — Max Pulse                      ░░░░░░░░░░ 0.00

==============================================================
```

### Adversarial: Impossible / Out-of-Range values

`{'genre': ['polka'], 'mood': ['yodeling'], 'energy': 2.0, 'tempo_bpm': 300, 'acousticness': -1.0}`

```
==============================================================
  🎵  Top Music Recommendations
  for  genre=polka · mood=yodeling · energy=2.0 · tempo_bpm=300 · acousticness=-1.0
==============================================================

  1. Iron Verdict — Ashen Crown                ░░░░░░░░░░ 0.03
        ├─ genre 'metal' not in your preferences (+0.00)
        ├─ acousticness 0.03 vs target -1.0 (match 0%, +0.00)
        ├─ energy 0.97 vs target 2.0 (match 0%, +0.00)
        ├─ mood 'aggressive' not in your preferences (+0.00)
        └─ tempo_bpm 172.0 vs target 300 (match 73%, +0.03)

  2. Storm Runner — Voltline                   ░░░░░░░░░░ 0.02
        ├─ genre 'rock' not in your preferences (+0.00)
        ├─ acousticness 0.1 vs target -1.0 (match 0%, +0.00)
        ├─ energy 0.91 vs target 2.0 (match 0%, +0.00)
        ├─ mood 'intense' not in your preferences (+0.00)
        └─ tempo_bpm 152.0 vs target 300 (match 62%, +0.02)

  3. Gym Hero — Max Pulse                      ░░░░░░░░░░ 0.02
        ├─ genre 'pop' not in your preferences (+0.00)
        ├─ acousticness 0.05 vs target -1.0 (match 0%, +0.00)
        ├─ energy 0.93 vs target 2.0 (match 0%, +0.00)
        ├─ mood 'intense' not in your preferences (+0.00)
        └─ tempo_bpm 132.0 vs target 300 (match 51%, +0.02)

  4. Pulse Reactor — Voltage Kids              ░░░░░░░░░░ 0.02
        ├─ genre 'techno' not in your preferences (+0.00)
        ├─ acousticness 0.04 vs target -1.0 (match 0%, +0.00)
        ├─ energy 0.95 vs target 2.0 (match 0%, +0.00)
        ├─ mood 'euphoric' not in your preferences (+0.00)
        └─ tempo_bpm 128.0 vs target 300 (match 49%, +0.02)

  5. Rooftop Lights — Indigo Parade            ░░░░░░░░░░ 0.02
        ├─ genre 'indie pop' not in your preferences (+0.00)
        ├─ acousticness 0.35 vs target -1.0 (match 0%, +0.00)
        ├─ energy 0.76 vs target 2.0 (match 0%, +0.00)
        ├─ mood 'happy' not in your preferences (+0.00)
        └─ tempo_bpm 124.0 vs target 300 (match 47%, +0.02)

==============================================================
```

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



