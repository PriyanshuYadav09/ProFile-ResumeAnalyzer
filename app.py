import os
import base64
import streamlit as st
from utils.analyzer import extract_text_from_pdf, extract_skills, assess_tone, load_skill_set
from utils.visualizer import create_radar_chart, draw_tone_slider
from utils.parser import extract_name, extract_email, calculate_ats_score
from collections import Counter

# Page configuration
st.set_page_config(
    page_title="ProFile – Resume Analyzer",
    page_icon="🧠",
    layout="wide"
)

# Custom CSS
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
st.sidebar.image("assets/img.jpg", width=180, caption="ProFile", use_column_width=False)
st.sidebar.title("Navigation")
choice = st.sidebar.radio("Go to", ["Home", "About"])

# Directory for file upload
UPLOAD_DIR = "uploaded"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Personality quality keyword base
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
        f'<iframe src="data:application/pdf;base64,{base64_pdf}" '
        f'width="600" height="600" type="application/pdf"></iframe>',
        unsafe_allow_html=True
    )

# Home Page
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

        # Candidate Info
        st.subheader("🔍 Candidate Details")
        st.write(f"**Name:** {extract_name(resume_text)}")
        st.write(f"**Email:** {extract_email(resume_text)}")

        # Skills
        st.subheader("🛠️ Extracted Skills")
        if extracted_skills:
            st.write(", ".join(extracted_skills))
        else:
            st.warning("No matching skills found in the resume.")

        # Traits
        st.subheader("🧠 Predicted Personality Traits")
        qualities = predict_qualities(extracted_skills, quality_keywords)
        if qualities:
            for trait, count in qualities.items():
                st.markdown(f"- **{trait}** ({count})")
            create_radar_chart(qualities)
        else:
            st.info("No traits identified from extracted skills.")

        # Tone
        st.subheader("🗣️ Resume Tone")
        tone_label, polarity = assess_tone(resume_text)
        st.write(f"**Tone:** {tone_label}")
        st.image(draw_tone_slider(polarity), use_column_width=True)

        # ATS Score
        st.subheader("📊 ATS Score")
        ats = calculate_ats_score(resume_text, extracted_skills)
        st.progress(ats)
        st.success(f"Estimated ATS Score: {ats}%")
        
        # PDF Report Download
        from utils.report_utils import generate_pdf_report

        if st.button("📥 Download Analysis Report as PDF"):
            pdf_path = generate_pdf_report(
                name=extract_name(resume_text),
                email=extract_email(resume_text),
                skills=extracted_skills,
                traits=qualities,
                tone=tone_label,
                ats_score=ats
            )
            with open(pdf_path, "rb") as f:
                st.download_button("Download Report", f, file_name="ProFile_Report.pdf")

        # Job Match Section
        st.subheader("🧪 Job Description Match")

        with st.form(key="job_match_form"):
            job_desc = st.text_area("Paste Job Description Here")
            match_button = st.form_submit_button("🔍 Match with Job Description")

        if match_button and job_desc.strip():
            jd_skills = extract_skills(job_desc, skill_set)
    
            if not jd_skills:
                st.error("No recognizable skills found in the job description.")
            else:
                match = [s for s in jd_skills if s in extracted_skills]
                missing = [s for s in jd_skills if s not in extracted_skills]
                match_score = int((len(match) / len(jd_skills)) * 100)

                st.write(f"📋 Skills Found in JD: {', '.join(jd_skills)}")
                st.write(f"✅ Matching Skills: {', '.join(match) if match else 'None'}")
                st.write(f"❌ Missing Skills: {', '.join(missing) if missing else 'None'}")

                if len(jd_skills) < 3:
                    st.warning("⚠️ Job description has very few recognized skills — score may not be meaningful.")
                elif match_score < 40:
                    st.error(f"📉 Resume Match Score: {match_score}% (Low match)")
                elif match_score < 70:
                    st.info(f"📈 Resume Match Score: {match_score}% (Partial match)")
                else:
                    st.success(f"✅ Resume Match Score: {match_score}% (Good match)")
            if len(jd_skills) == 1 and match_score == 100:
                st.warning("⚠️ Only 1 skill matched, 100% score may not be reliable.")






# About Page
elif choice == "About":
    st.title("ℹ️ About ProFile")
    st.markdown("""
    **ProFile** is an AI-powered resume analyzer that extracts skills, analyzes tone, and predicts professional traits.

    **Tech Stack:**
    - Python, Streamlit
    - spaCy, TextBlob, Matplotlib
    - PDFMiner, PIL
    - `skills.txt` dataset for matching

    **Use Case:**  
    Helpful for job seekers to improve resumes and for recruiters to screen applicants.
    """)


