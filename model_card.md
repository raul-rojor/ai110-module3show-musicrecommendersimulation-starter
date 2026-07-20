# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

Music Matcher

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

The recommender is designed to recommend songs to users based on their musical preferences. The recommender is designed for music listeners who want to find new songs they are likely to enjoy. The recommender assumes the user can adequately convey their music taste through qualitative and quantitative descriptions on various measures of music. This algorithm is only meant to simulate recommenders that may be used in streaming apps and explore their possibilities and limitations/considerations.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

The scoring of songs based on user music preferences is based on weighing out how well different musical aspects of different songs match the user's taste and then recommending the songs that best overall match their taste profile. The scoring is done by quantifying musical factors. The starter logic was expanded to include more music features, songs, and changes to weigh musical similarities differently.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

The model uses a variety of possible user profiles with different tastes and of songs with different styles/sounds. The user tastes and songs include many different genres and moods which dont always overlap between the two purposefully in order to test inexact matches between song catalogs and tastes. I would argue that musical taste can be portrayed in so many different ways that there are certainly parts of musical taste not translated well in this model's act of finding songs the user would like. However, I still believe the model and dataset capure musical taste generally well, well enough for most users to find their taste reflected adequately in the songs recommended to them.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition 

Users with popular genre and mood preferences as well as users with uncontradictory/niche preferences as seen in their relative preferences between music features are served well by this recommender. When a user's preferred genres/moods are supported by their preferred energy, acousticness, and other quantitive measures, scoring correctly captures their taste and recommends well-fitting songs. In these cases, the recommendations match my musical intuition.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

There are many limitations to my system. Firstly, genre is binary while being weighed the most heavily, causing an all-or-nothing effect in matching songs to tastes. Additionally, niche tastes, particularly niche genre and mood preferences, are underrepresented in the present song catalog and are therefore difficult to find strong song matches for. These niche-enjoying users tend to get confidently-outputted songs they are likely to be indifferent to at best and off-putted by at worst. Finally, in my own estimation, most music listeners have a variety of different so-called "tastes." A user may like high energy rock songs and low energy lofi songs simultaneously. This complicated reality is hard to capture with such a simple scoring logic as the one currently employed.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

I tested user profiles that reflect basic, non-contradictory (or common) music tastes as well a user with a seemingly contradictory music taste and a couple users with no taste or an impossible taste (according to the model's format). In the recommendations I looked for songs that closely match in both genre and what I pieced together to mean an either 'upbeat' or 'downbeat' sound to the user's taste. Users with common music tastes were recommended very well-matching songs across music features. I wasn't suprised by the recommendations given to the other users because I understood how my model's scoring logic works, but I noticed that for the confusing taste profile, the mood was very different from that of the recommended songs and that recommendations were random for edge-case user profiles. I believe detailing comparisons between particular profiles is unnecessary because the results for different profile types is explained effectively above.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

I would improve the model by first adding a much longer song catalog that would reflect a real streaming platforms catalog size. This would help to test the recommender in a real-world setting, potentially handling the issue of niche or complex user tastes. Besides that, I would construct multiple music taste profiles for each user (maybe with a weight of these different profiles in choosing what songs to recommend overall)since a user may like many contradicting music styles at the same time. Finally, I would add an option for the user to choose how experimental trelative to their own taste they would want their song recommendations to be.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps 

I learned that recommender systems have to balance a myriad of tradeoffs and are therefore encouraged to be complex. I now understand why recommender systems in real platforms tend to use deep learning algorithm to push recommendations to users. Without these complicated models, recommendations are more likely to miss the nuance inherent to user preferences. It is therefore clear to me now how music recommenders are very possibly well represented or even implemented as prediction models just like large language models where the best-fitting embedding (token) is chosen from past embeddings (tokens) as context. This makes me wonder if songs and user preferences can be embedded to be turned into vectors and similarities can then be calculated. If so, I wonder if streaming platforms employ this technique, especially with the recent advancements in large-language and multimodal AI models.