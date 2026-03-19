from pylatex import Document, Section, Command
from pylatex.utils import NoEscape

def create_pdf(content):
    geometry_options = {"margin": "1in"}
    doc = Document(documentclass="IEEEtran", geometry_options=geometry_options)

    # ----------------------------
    # TITLE
    # ----------------------------
    doc.preamble.append(Command("title", "AI Generated Research Paper"))
    doc.preamble.append(Command("author", "Your Name"))
    doc.preamble.append(Command("date", NoEscape(r"\today")))
    doc.append(NoEscape(r"\maketitle"))

    # ----------------------------
    # MAIN SECTIONS
    # ----------------------------
    for section, text in content.items():
        if section != "References":
            try:
                with doc.create(Section(section)):
                    doc.append(text if text else "No content available.")
            except Exception as e:
                doc.append(f"Error in section {section}: {e}")

    # ----------------------------
    # REFERENCES (SAFE FIX 🔥)
    # ----------------------------
    doc.append(NoEscape(r"\section*{References}"))

    references = content.get("References", None)

    if references and references.strip():
        doc.append(NoEscape(references))
    else:
        doc.append("No references available.")

    # ----------------------------
    # GENERATE PDF
    # ----------------------------
    try:
        doc.generate_pdf("research_paper", clean_tex=False)
    except Exception as e:
        print("❌ PDF generation failed:", e)