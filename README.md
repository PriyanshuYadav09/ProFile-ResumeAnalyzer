# 🧠 ProFile – Smart Resume Analyzer

ProFile is an AI-powered web application that analyzes resumes and provides:
- ✅ Skill extraction using NLP
- 📊 Personality trait prediction
- 🎯 ATS score estimation
- 🗣️ Tone analysis
- 🧪 Job description match comparison
- 📄 Downloadable PDF analysis reports

Built with `Python`, `Streamlit`, and `spaCy`, it's designed for job seekers, recruiters, and career mentors.

---

## 🚀 Features

| Feature                        | Description |
|-------------------------------|-------------|
| 📄 Resume Upload              | Upload a PDF resume and analyze it in real-time |
| 🛠️ Skill Extraction           | Extract technical and soft skills using a skill dataset |
| 🧠 Trait Prediction            | Predict personality traits based on extracted keywords |
| 🗣️ Tone Analysis              | Detect positivity/neutrality of the resume tone |
| 📊 Skill Frequency Chart      | Bar chart showing most mentioned skills |
| 📈 ATS Score                  | Estimate resume performance on ATS systems |
| 🧪 JD Matching                | Compare resume with job description skills |
| 📥 PDF Report Generation      | Download a summary report of the analysis |

---

## 🛠️ Tech Stack

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [spaCy](https://spacy.io/)
- [TextBlob](https://textblob.readthedocs.io/)
- [Matplotlib](https://matplotlib.org/)
- [PDFMiner](https://pypi.org/project/pdfminer.six/)
- [FPDF](https://py-pdf.github.io/fpdf2/)

---

## 📂 Folder Structure

ProFile/
├── app.py
├── requirements.txt
├── skills.txt
├── uploaded/
├── assets/
│ └── img.jpg
├── utils/
│ ├── analyzer.py
│ ├── parser.py
│ ├── visualizer.py
│ └── report_utils.py


---

## 🧪 How to Run Locally

```bash
# Clone the repo
git clone https://github.com/PriyanshuYadav09/ProFile-ResumeAnalyzer
cd ProFile

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
