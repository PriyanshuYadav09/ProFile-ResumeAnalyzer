import os
import base64
import streamlit as st
import matplotlib.pyplot as plt
from collections import Counter
from utils.analyzer import extract_text_from_pdf, extract_skills, assess_tone, load_skill_set
from utils.parser import extract_name, extract_email, calculate_ats_score_dynamic, extract_job_title_from_jd
from utils.visualizer import create_radar_chart, draw_tone_slider
from utils.report_utils import generate_pdf_report

# Setup
st.set_page_config(page_title="ProFile – Resume Analyzer", page_icon="🧠", layout="wide")

UPLOAD_DIR = "uploaded"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Custom styles
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background-color: #2f3542;
        color: white;
    }
    .sidebar-logo {
        display: block;
        margin-left: auto;
        margin-right: auto;
        border-radius: 10px;
        margin-top: 10px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.image("assets/img.jpg", width=180, caption="ProFile")
st.sidebar.title("Navigation")
choice = st.sidebar.radio("Go to", ["Home", "About"])

# Quality keywords
quality_keywords = {
    "Team Player": ['teamwork', 'collaboration', 'supportive', 'communication'],
    "Leader": ['leadership', 'strategic', 'mentoring', 'decision making'],
    "Creative": ['design', 'creative', 'innovation', 'content'],
    "Organized": ['planning', 'organized', 'scheduling', 'time management'],
    "Analytical": ['analysis', 'data', 'research', 'problem solving']
}

def predict_qualities(skills, quality_datasets):
    score = Counter()
    for skill in skills:
        for quality, words in quality_datasets.items():
            if any(w.lower() in skill.lower() for w in words):
                score[quality] += 1
    return dict(score.most_common())

def show_pdf(path):
    with open(path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    st.markdown(
        f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="600" height="600" type="application/pdf"></iframe>',
        unsafe_allow_html=True
    )

if choice == "Home":
    st.title("📄 Upload Your Resume")
    pdf_file = st.file_uploader("Upload a PDF Resume", type=["pdf"])

    if pdf_file:
        path = os.path.join(UPLOAD_DIR, pdf_file.name)
        with open(path, "wb") as f:
            f.write(pdf_file.getbuffer())

        st.success("Resume uploaded successfully.")
        show_pdf(path)

        # Analyze resume
        resume_text = extract_text_from_pdf(path)
        skill_set = load_skill_set()
        extracted_skills = extract_skills(resume_text, skill_set)

        name = extract_name(resume_text)
        email = extract_email(resume_text)

        st.subheader("🔍 Candidate Details")
        st.write(f"**Name:** {name}")
        st.write(f"**Email:** {email}")

        st.subheader("🛠️ Extracted Skills")
        st.write(", ".join(extracted_skills) if extracted_skills else "No matching skills found.")

        st.subheader("📊 Skill Frequency")
        skill_freq = {skill: resume_text.lower().count(skill) for skill in extracted_skills}
        sorted_skills = dict(sorted(skill_freq.items(), key=lambda x: x[1], reverse=True))
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.barh(list(sorted_skills.keys()), list(sorted_skills.values()), color="skyblue")
        ax.set_xlabel("Frequency")
        ax.invert_yaxis()
        st.pyplot(fig)

        st.subheader("🧠 Predicted Personality Traits")
        qualities = predict_qualities(extracted_skills, quality_keywords)
        if qualities:
            for trait, count in qualities.items():
                st.markdown(f"- **{trait}** ({count})")
            create_radar_chart(qualities)
        else:
            st.info("No traits identified from extracted skills.")

        st.subheader("🗣️ Resume Tone")
        tone_label, polarity = assess_tone(resume_text)
        st.write(f"**Tone:** {tone_label}")
        st.image(draw_tone_slider(polarity), use_column_width=True)

        # Job description matching
        st.subheader("🧪 Job Description Match")
        with st.form(key="job_match_form"):
            job_desc = st.text_area("Paste Job Description Here")
            match_button = st.form_submit_button("🔍 Match with Job Description")

        if match_button and job_desc.strip():
            jd_skills = extract_skills(job_desc, skill_set)
            match = [s for s in jd_skills if s in extracted_skills]
            missing = [s for s in jd_skills if s not in extracted_skills]
            match_score = int((len(match) / len(jd_skills)) * 100) if jd_skills else 0

            st.write(f"📋 Skills Found in JD: {', '.join(jd_skills)}")
            st.write(f"✅ Matching Skills: {', '.join(match) if match else 'None'}")
            st.write(f"❌ Missing Skills: {', '.join(missing) if missing else 'None'}")
            st.success(f"📈 Resume Match Score: {match_score}%")

            # Extract job title from JD
            title = extract_job_title_from_jd(job_desc)
            st.subheader(f"📊 ATS Score for: {title}")
            ats_score = calculate_ats_score_dynamic(resume_text, job_desc, skill_set)
            st.progress(ats_score)
            st.success(f"Estimated ATS Score: {ats_score}%")

            # PDF Report Download
            pdf_path = generate_pdf_report(
                name=name,
                email=email,
                skills=extracted_skills,
                traits=qualities,
                tone=tone_label,
                ats_score=ats_score
            )

            with open(pdf_path, "rb") as f:
                pdf_bytes = f.read()

            st.download_button(
                label="📥 Download Analysis Report as PDF",
                data=pdf_bytes,
                file_name="ProFile_Resume_Report.pdf",
                mime="application/pdf"
            )



elif choice == "About":
    st.title("ℹ️ About ProFile")
    st.markdown("""
    **ProFile** is an AI-powered resume analyzer that extracts skills, analyzes tone, predicts personality traits,
    and compares your resume against job descriptions using smart scoring logic.

    Built using:
    - Python & Streamlit
    - spaCy, TextBlob, Matplotlib
    - PDFMiner, FPDF

    Created for professionals and job seekers to improve resume visibility and content.
    """)



