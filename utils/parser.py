# utils/parser.py
import re
from textblob import TextBlob
from .analyzer import extract_skills

# ✅ Extract candidate name (rudimentary, improve later with NLP)
def extract_name(text):
    lines = text.strip().split("\n")
    for line in lines:
        line = line.strip()
        if line and len(line.split()) <= 4 and all(x[0].isupper() for x in line.split() if x):
            return line
    return "Not Found"

# ✅ Extract email address
def extract_email(text):
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}", text)
    return match.group(0) if match else "Not Found"

def extract_job_title_from_jd(jd_text):
    lines = jd_text.strip().lower().split('\n')
    for line in lines[:3]:
        match = re.search(r'looking for a\s+(.*?)(?:\.|,| at| to| for)', line)
        if match:
            return match.group(1).title().strip()
    return "Job Role"

def calculate_ats_score_dynamic(resume_text, jd_text, skill_set):
    resume_text = resume_text.lower()
    jd_text = jd_text.lower()

    resume_skills = extract_skills(resume_text, skill_set)
    jd_skills = extract_skills(jd_text, skill_set)

    if not jd_skills:
        return 0

    # Skill match score (60%)
    matched = [s for s in jd_skills if s in resume_skills]
    skill_score = int((len(matched) / len(jd_skills)) * 60)

    # Frequency bonus (10%)
    freq_score = 0
    for skill in matched:
        freq_score += resume_text.count(skill)
    freq_score = min(freq_score, 10)

    # Tone score (10%)
    polarity = TextBlob(resume_text).sentiment.polarity
    tone_score = 10 if polarity >= 0.2 else 5 if polarity >= 0 else 0

    # Bonus keywords (10%)
    bonus_keywords = ['git', 'sql', 'docker', 'cloud', 'aws', 'github']
    bonus_score = sum(1 for word in bonus_keywords if word in resume_text)
    bonus_score = min(bonus_score, 10)

    total_score = skill_score + freq_score + tone_score + bonus_score
    return min(total_score, 100)




def clean_resume_text(text):
    # Remove multiple spaces/newlines
    return re.sub(r'\s+', ' ', text)
