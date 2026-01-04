import pandas as pd
import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from nlp.preprocess import preprocess

# Ensure models folder exists
os.makedirs("models", exist_ok=True)

# Load dataset
df = pd.read_csv("data/emails.csv")

# Preprocess text
df["clean"] = df["text"].apply(preprocess)

# Encode labels
le = LabelEncoder()
y = le.fit_transform(df["label"])

# TF-IDF Vectorizer
tfidf = TfidfVectorizer(ngram_range=(1, 2), max_features=5000)
X = tfidf.fit_transform(df["clean"])

# Train model
model = RandomForestClassifier(
    n_estimators=300,
    class_weight="balanced",
    random_state=42
)
model.fit(X, y)

# Save everything
joblib.dump(tfidf, "models/tfidf.pkl")
joblib.dump(model, "models/rf_model.pkl")
joblib.dump(le, "models/label_encoder.pkl")

print("Model trained successfully")
