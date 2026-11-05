"""Classical ML: TF-IDF + Logistic Regression document categoriser (see ml/train_classifier.py)."""
import os
import joblib

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "ml", "doc_classifier.joblib")
_pipe = None


def classify(text: str) -> str:
    global _pipe
    if _pipe is None:
        if not os.path.exists(MODEL_PATH):
            return "Uncategorized"
        _pipe = joblib.load(MODEL_PATH)
    return str(_pipe.predict([text[:5000]])[0])
