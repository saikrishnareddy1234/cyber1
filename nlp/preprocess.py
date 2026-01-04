import re
import unicodedata
import nltk
from nltk.corpus import stopwords

# ✅ Ensure stopwords are available (important for Streamlit Cloud)
try:
    stopwords.words("english")
except LookupError:
    nltk.download("stopwords")

# Stopwords
STOPWORDS = set(stopwords.words("english")) | set(stopwords.words("french"))
TELUGU_STOPWORDS = {"మరియు", "ఇది", "అది", "కానీ"}

def preprocess(text):
    # Normalize unicode (important for multilingual text)
    text = unicodedata.normalize("NFKD", text).lower()

    # Remove URLs
    text = re.sub(r"http\S+", "", text)

    # Keep English + Telugu characters only
    text = re.sub(r"[^a-zA-Z\u0C00-\u0C7F\s]", "", text)

    # Tokenize
    tokens = text.split()

    # Remove stopwords
    tokens = [
        t for t in tokens
        if t not in STOPWORDS and t not in TELUGU_STOPWORDS
    ]

    return " ".join(tokens)
