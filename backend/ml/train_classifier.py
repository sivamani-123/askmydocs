"""Train the document category model. Run: python ml/train_classifier.py
Replace SEED with your own labelled data for better accuracy."""
import os
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline

SEED = {
    "Finance": ["quarterly revenue and profit margin report", "invoice payment due balance sheet", "budget forecast expenses investment returns",
                "tax filing audit cash flow statement", "loan interest rate credit risk assessment", "stock dividend earnings per share"],
    "Legal": ["this agreement is governed by the laws of the state", "the parties hereby agree to indemnify and hold harmless", "confidentiality clause termination liability",
              "intellectual property license warranty breach", "plaintiff defendant court jurisdiction ruling", "terms and conditions privacy compliance regulation"],
    "Technical": ["the api returns a json response with status code", "install dependencies and configure the server", "neural network training gradient descent model",
                  "database schema index query performance", "deploy docker container kubernetes cluster", "software architecture microservices latency"],
    "HR": ["employee onboarding leave policy and benefits", "performance review and promotion criteria", "recruitment interview candidate hiring process",
           "payroll attendance holiday calendar workplace conduct", "training and development career growth plan", "resignation notice period exit interview"],
}

X = [t for texts in SEED.values() for t in texts]
y = [label for label, texts in SEED.items() for _ in texts]
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
pipe = make_pipeline(TfidfVectorizer(ngram_range=(1, 2), stop_words="english"), LogisticRegression(max_iter=1000))
pipe.fit(Xtr, ytr)
print(classification_report(yte, pipe.predict(Xte), zero_division=0))
pipe.fit(X, y)
out = os.path.join(os.path.dirname(__file__), "doc_classifier.joblib")
joblib.dump(pipe, out)
print("Saved", out)
