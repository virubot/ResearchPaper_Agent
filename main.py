from fetch_semantic import fetch_papers
from bibtex_parser import generate_bibtex
from plagiarism import check_plagiarism
from latex_writer import create_pdf
from agents import research_agent, analysis_agent, writer_agent
from rag import RAG
from pdf_reader import download_pdf, extract_text_from_pdf


# ----------------------------
# INPUT
# ----------------------------
topic = input("Enter research topic: ")

# ----------------------------
# STEP 1: FETCH PAPERS
# ----------------------------
papers = fetch_papers(topic)

if not papers:
    print("⚠️ No papers found. Using fallback data...")
    papers = [
        {
            "id": 1,
            "title": f"Study on {topic}",
            "abstract": f"This paper discusses {topic} using AI techniques.",
            "year": 2024,
            "doi": "N/A",
            "pdf": None
        }
    ]

# ----------------------------
# STEP 2: PREPARE CHUNKS
# ----------------------------
chunks = []

for i, p in enumerate(papers):
    text = ""

    print(f"\n📄 Processing Paper {i+1}")
    print(f"Title: {p.get('title')}")
    print(f"PDF: {p.get('pdf')}")
    print(f"Has Abstract: {bool(p.get('abstract'))}")

    # Try PDF
    if p.get("pdf"):
        try:
            print("📥 Downloading PDF...")
            file_path = download_pdf(p["pdf"], f"paper_{i}.pdf")

            if file_path:
                text = extract_text_from_pdf(file_path)
                text = text[:5000]
        except Exception as e:
            print("⚠️ PDF failed:", e)

    # Fallback → Abstract
    if not text.strip() and p.get("abstract"):
        text = p["abstract"]

    # Fallback → Title
    if not text.strip():
        text = p.get("title", "")

    # Skip if empty
    if not text.strip():
        print("⚠️ Skipping empty paper")
        continue

    # Chunking
    sentences = text.split(".")
    for j in range(0, len(sentences), 3):
        chunk = ". ".join(sentences[j:j+3])

        if chunk.strip():
            chunks.append(f"[{p['id']}] {chunk}")

# ----------------------------
# FINAL SAFETY
# ----------------------------
if not chunks:
    print("❌ No usable data found. Exiting...")
    exit()

# Limit chunks
chunks = chunks[:100]

print(f"\n✅ Total chunks created: {len(chunks)}")

# ----------------------------
# STEP 3: RAG SETUP
# ----------------------------
rag = RAG()
rag.add_documents(chunks)

relevant_chunks = rag.query(topic, k=5)

if not relevant_chunks:
    print("⚠️ No relevant chunks found. Using fallback context.")
    rag_context = "Basic information about the topic."
else:
    rag_context = "\n".join(relevant_chunks)

# 🔥 LIMIT CONTEXT
rag_context = rag_context[:4000]

print(f"✅ Using top {len(relevant_chunks)} chunks")

# ----------------------------
# STEP 4: MULTI-AGENT PIPELINE
# ----------------------------
print("\n🤖 Running Research Agent...")
research_summary = research_agent(topic, rag_context)

print("\n🧠 Running Analysis Agent...")
analysis = analysis_agent(topic, research_summary)

print("\n✍️ Running Writer Agent...")
content = writer_agent(topic, rag_context)

# ----------------------------
# SAFETY: WRITER OUTPUT
# ----------------------------
if not content or not isinstance(content, dict):
    print("⚠️ Writer agent failed. Using fallback content.")
    content = {
        "Introduction": "Content generation failed.",
        "Conclusion": "Content generation failed."
    }

# ----------------------------
# STEP 5: PLAGIARISM CHECK
# ----------------------------
intro = content.get("Introduction", "")
similarity = check_plagiarism(intro, [rag_context])
print(f"\n📊 Plagiarism Score: {similarity:.2f}")

# ----------------------------
# STEP 6: REFERENCES
# ----------------------------
try:
    bibtex = generate_bibtex(papers)

    if bibtex and bibtex.strip():
        content["References"] = bibtex
    else:
        content["References"] = "No references available"

except Exception as e:
    print("⚠️ Reference generation failed:", e)
    content["References"] = "No references available"

# ----------------------------
# STEP 7: GENERATE PDF
# ----------------------------
try:
    create_pdf(content)
    print("\n✅ Research paper generated: research_paper.pdf")

except Exception as e:
    print("❌ PDF generation failed:", e)