# FAQ Chatbot — CodeAlpha Task 2

A simple FAQ chatbot that matches user questions to the closest FAQ using
TF-IDF vectorization and cosine similarity, with spaCy for text preprocessing.

## Files
- `faq_data.json` — the FAQ dataset (sample: college admissions topic). **Replace this with your own topic's Q&A pairs.**
- `chatbot.py` — core logic: preprocessing + matching. Run directly for a terminal chatbot.
- `app.py` — optional Streamlit web UI.
- `requirements.txt` — Python dependencies.

## Setup

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## Run in terminal

```bash
python chatbot.py
```

## Run with web UI

```bash
streamlit run app.py
```

## Customizing for your own topic

1. Open `faq_data.json` and replace the questions/answers with your chosen topic
   (product support, a course, a service, etc.). Keep the same
   `{"question": "...", "answer": "..."}` structure.
2. That's it — `chatbot.py` and `app.py` will automatically use the new data.

## How it works

1. **Preprocessing**: Every FAQ question and user query is lowercased,
   stripped of stopwords/punctuation, and lemmatized using spaCy.
2. **Vectorization**: All FAQ questions are converted into TF-IDF vectors.
3. **Matching**: A user's query is vectorized the same way, then compared
   to every FAQ question using cosine similarity.
4. **Response**: The FAQ with the highest similarity score is returned as
   the answer, as long as it clears a minimum confidence threshold
   (`SIMILARITY_THRESHOLD` in `chatbot.py`). Otherwise, a fallback message
   is shown.

## Notes for your internship report

- You can mention **NLTK/spaCy** for preprocessing (this uses spaCy).
- Matching technique: **TF-IDF + cosine similarity** (a lightweight, explainable
  intent-matching approach — no deep learning needed for FAQ bots this size).
- The Streamlit app fulfills the "optional chat UI" requirement in the task.
