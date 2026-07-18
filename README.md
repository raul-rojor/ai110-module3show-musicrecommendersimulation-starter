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
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

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



