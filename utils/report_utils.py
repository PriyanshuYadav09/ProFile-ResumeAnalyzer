from fpdf import FPDF

def generate_pdf_report(name, email, skills, traits, tone, ats_score, output_path="report.pdf"):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Resume Analysis Report", ln=True, align='C')

    pdf.ln(10)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Name: {name}", ln=True)
    pdf.cell(0, 10, f"Email: {email}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Extracted Skills:", ln=True)
    pdf.set_font("Arial", '', 12)
    for skill in skills:
        pdf.cell(0, 8, f"- {skill}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Personality Traits:", ln=True)
    pdf.set_font("Arial", '', 12)
    for trait, count in traits.items():
        pdf.cell(0, 8, f"- {trait} ({count})", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"Tone: {tone}", ln=True)
    pdf.cell(0, 10, f"ATS Score: {ats_score}%", ln=True)

    pdf.output(output_path)
    return output_path
