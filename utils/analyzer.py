import spacy
from pdfminer.high_level import extract_text
from textblob import TextBlob

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Load skills from file
def load_skill_set(path="data/skills.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return set(line.strip().lower() for line in f if line.strip())

def extract_text_from_pdf(path):
    return extract_text(path)

def extract_skills(text, skill_set):
    text = text.lower()
    found = []
    for skill in skill_set:
        if skill.lower() in text:
            found.append(skill)
    return list(set(found))

def assess_tone(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity >= 0.5:
        return "Positive", polarity
    elif polarity > 0:
        return "Slightly Positive", polarity
    elif polarity == 0:
        return "Neutral", polarity
    elif polarity > -0.5:
        return "Slightly Negative", polarity
    else:
        return "Negative", polarity


