import streamlit as st
from fetch_semantic import fetch_papers
from bibtex_parser import generate_bibtex
from plagiarism import check_plagiarism
from latex_writer import create_pdf
from agents import research_agent, analysis_agent, writer_agent
from rag import RAG
from pdf_reader import download_pdf, extract_text_from_pdf

st.set_page_config(page_title="AI Research Generator", layout="wide")

st.title("🤖 AI Research Paper Generator")

topic = st.text_input("Enter Research Topic")

if st.button("Generate Research Paper"):

    if not topic:
        st.warning("Please enter a topic")
        st.stop()

    # ----------------------------
    # FETCH PAPERS
    # ----------------------------
    st.info("📥 Fetching papers...")
    papers = fetch_papers(topic)

    if not papers:
        st.error("No papers found. Try another topic.")
        st.stop()

    # ----------------------------
    # CHUNKING
    # ----------------------------
    chunks = []

    for i, p in enumerate(papers):
        text = ""

        if p.get("pdf"):
            try:
                file_path = download_pdf(p["pdf"], f"paper_{i}.pdf")
                if file_path:
                    text = extract_text_from_pdf(file_path)
                    text = text[:5000]
            except Exception:
                st.warning(f"PDF failed for paper {i+1}")

        if not text.strip():
            text = p.get("abstract") or p.get("title", "")

        sentences = text.split(".")
        for j in range(0, len(sentences), 3):
            chunk = ". ".join(sentences[j:j+3])
            if chunk.strip():
                chunks.append(f"[{p['id']}] {chunk}")

    if not chunks:
        st.error("No usable data found.")
        st.stop()

    chunks = chunks[:100]

    # ----------------------------
    # RAG
    # ----------------------------
    rag = RAG()
    rag.add_documents(chunks)

    relevant_chunks = rag.query(topic, k=5)

    if not relevant_chunks:
        rag_context = "Basic information about the topic."
    else:
        rag_context = "\n".join(relevant_chunks)

    # 🔥 LIMIT CONTEXT
    rag_context = rag_context[:4000]

    # ----------------------------
    # AGENTS
    # ----------------------------
    st.info("🤖 Running Research Agent...")
    research_summary = research_agent(topic, rag_context)

    st.info("🧠 Running Analysis Agent...")
    analysis = analysis_agent(topic, research_summary)

    st.info("✍️ Writing Paper...")
    content = writer_agent(topic, rag_context)

    # ----------------------------
    # SAFETY CHECK
    # ----------------------------
    if not content or not isinstance(content, dict):
        st.error("⚠️ Content generation failed.")
        st.stop()

    # ----------------------------
    # 🔥 PLAGIARISM CHECK (FIXED)
    # ----------------------------
    try:
        intro = content.get("Introduction", "")
        similarity = check_plagiarism(intro, [rag_context])

        st.subheader("📊 Plagiarism Score")
        st.metric("Similarity Score", f"{similarity:.2f}")

    except Exception:
        st.warning("⚠️ Could not calculate plagiarism score")

    # ----------------------------
    # REFERENCES
    # ----------------------------
    try:
        bibtex = generate_bibtex(papers)

        if bibtex and bibtex.strip():
            content["References"] = bibtex
        else:
            content["References"] = "No references available"

    except Exception:
        st.warning("⚠️ Failed to generate references")
        content["References"] = "No references available"

    # ----------------------------
    # RESULTS DISPLAY
    # ----------------------------
    st.success("✅ Paper Generated!")

    st.subheader("📄 Introduction")
    st.write(content.get("Introduction", ""))

    st.subheader("📄 Conclusion")
    st.write(content.get("Conclusion", ""))

    # ----------------------------
    # PDF GENERATION
    # ----------------------------
    try:
        create_pdf(content)

        with open("research_paper.pdf", "rb") as f:
            st.download_button(
                "📥 Download PDF",
                f,
                file_name="research_paper.pdf"
            )

    except Exception as e:
        st.error(f"❌ PDF generation failed: {e}")