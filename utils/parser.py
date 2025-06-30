# utils/parser.py
import re

def extract_name(text):
    """Try to extract a full name from the top of the resume."""
    lines = text.strip().split('\n')
    for line in lines[:10]:
        clean_line = line.strip()
        if re.match(r'^[A-Z][a-z]+\s[A-Z][a-z]+$', clean_line):
            return clean_line
    return "Not Found"

def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return match.group(0) if match else "Not Found"

def calculate_ats_score(text, extracted_skills):
    """Basic ATS score based on matched skill occurrences."""
    if not extracted_skills:
        return 0
    text_lower = text.lower()
    matched = sum(1 for skill in extracted_skills if skill in text_lower)
    return int((matched / len(extracted_skills)) * 100)


def clean_resume_text(text):
    # Remove multiple spaces/newlines
    return re.sub(r'\s+', ' ', text)
