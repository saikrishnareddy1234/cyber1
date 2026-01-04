
import re, unicodedata
from nltk.corpus import stopwords

STOPWORDS = set(stopwords.words("english")) | set(stopwords.words("french"))
TELUGU_STOPWORDS = {"మరియు","ఇది","అది","కానీ"}

def preprocess(text):
    text = unicodedata.normalize("NFKD", text).lower()
    text = re.sub(r"http\S+","",text)
    text = re.sub(r"[^a-zA-Z\u0C00-\u0C7F\s]","",text)
    tokens = text.split()
    tokens = [t for t in tokens if t not in STOPWORDS and t not in TELUGU_STOPWORDS]
    return " ".join(tokens)
