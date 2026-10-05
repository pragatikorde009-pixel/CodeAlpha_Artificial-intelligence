"""
FAQ Chatbot - Core Logic
CodeAlpha AI Internship - Task 2

Loads a FAQ dataset, preprocesses text using spaCy, and matches
user queries to the closest FAQ using TF-IDF + cosine similarity.
"""

import json
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load spaCy's small English model (run once: python -m spacy download en_core_web_sm)
nlp = spacy.load("en_core_web_sm")

# Similarity threshold below which we say "I don't know"
SIMILARITY_THRESHOLD = 0.25


class FAQChatbot:
    def __init__(self, faq_path="faq_data.json"):
        with open(faq_path, "r", encoding="utf-8") as f:
            self.faq_data = json.load(f)

        self.questions = [item["question"] for item in self.faq_data]
        self.processed_questions = [self._preprocess(q) for q in self.questions]

        self.vectorizer = TfidfVectorizer()
        self.faq_vectors = self.vectorizer.fit_transform(self.processed_questions)

    def _preprocess(self, text):
        """Lowercase, remove stopwords/punctuation, and lemmatize."""
        doc = nlp(text.lower())
        tokens = [
            token.lemma_
            for token in doc
            if not token.is_stop and not token.is_punct and not token.is_space
        ]
        return " ".join(tokens)

    def get_answer(self, user_query):
        """Return the best-matching FAQ answer, or a fallback message."""
        processed_query = self._preprocess(user_query)

        if not processed_query.strip():
            return "Could you please rephrase your question?"

        query_vector = self.vectorizer.transform([processed_query])
        similarities = cosine_similarity(query_vector, self.faq_vectors)[0]

        best_idx = similarities.argmax()
        best_score = similarities[best_idx]

        if best_score < SIMILARITY_THRESHOLD:
            return "Sorry, I don't have an answer for that. Please contact the support team."

        return self.faq_data[best_idx]["answer"]

    def get_answer_with_score(self, user_query):
        """Same as get_answer, but also returns the matched question + confidence (useful for debugging)."""
        processed_query = self._preprocess(user_query)
        query_vector = self.vectorizer.transform([processed_query])
        similarities = cosine_similarity(query_vector, self.faq_vectors)[0]

        best_idx = similarities.argmax()
        best_score = float(similarities[best_idx])

        if best_score < SIMILARITY_THRESHOLD:
            return None, None, best_score

        return self.faq_data[best_idx]["question"], self.faq_data[best_idx]["answer"], best_score


if __name__ == "__main__":
    bot = FAQChatbot("faq_data.json")
    print("FAQ Chatbot (type 'exit' to quit)\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("exit", "quit"):
            print("Bot: Goodbye!")
            break
        answer = bot.get_answer(user_input)
        print("Bot:", answer)
