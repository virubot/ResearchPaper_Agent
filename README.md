# 📄 AI Research Paper Generator 🚀

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Ollama](https://img.shields.io/badge/Ollama-Local%20LLMs-black.svg)](https://ollama.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red.svg)](https://streamlit.io/)
[![LaTeX](https://img.shields.io/badge/LaTeX-PDF_Gen-008080.svg)](https://www.latex-project.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> An AI-powered, multi-agent system that autonomously generates structured, IEEE-style research papers based on a given topic using local LLMs and Retrieval-Augmented Generation (RAG).

---

## 📖 Overview

Generating well-researched, structured, and accurately cited research papers manually can be overwhelming. This project automates the process by employing a **Multi-Agent Architecture** fueled by **Retrieval-Augmented Generation (RAG)**. 

By fetching relevant academic papers, eliminating hallucination with RAG, and formatting the output as an IEEE-standard PDF—all executing locally without relying on expensive APIs—this tool streamlines academic drafting.

---

## ✨ Key Features

- 🧠 **RAG-Powered Accuracy**: Submits context-rich prompts to LLMs, heavily reducing hallucinations.
- 🤖 **Multi-Agent Pipeline**: Distributes tasks among a Research Agent, Analysis Agent, and Writer Agent for high-quality, structured output.
- 🎓 **IEEE-Style Formatting**: Automates generation of professional academic papers via LaTeX.
- 📚 **Citation & Plagiarism**: Handles citations intuitively and natively checks against direct copying.
- 🔒 **100% Local Execution**: Powered by Ollama—no paid OpenAI/Anthropic APIs required!
- 🎛️ **Streamlit UI**: A clean, beginner-friendly web interface.

---

## 🛠️ Tech Stack

- **Language:** Python
- **LLM Engine:** Ollama (Local LLM Execution)
- **Vector Search:** FAISS / Sentence Transformers
- **Web App:** Streamlit
- **PDF Formatting:** LaTeX

---

## ⚙️ How It Works (Step-by-Step Pipeline)

1. **User Input:** The user provides a research topic via the Streamlit interface.
2. **Information Retrieval (`fetch_semantic.py` & `rag.py`):** The system searches semantic academic databases, downloads abstracts/metadata, and builds a local FAISS vector database.
3. **Research Agent (`agents.py`):** Queries the vector DB to retrieve the most factually relevant snippets.
4. **Analysis Agent (`agents.py`):** Analyzes the retrieved context, draws connections, and creates an outline for the paper.
5. **Writer Agent (`generator.py`):** Writes the paper section by section (Abstract, Introduction, Methodology, Results, Conclusion) with proper citations.
6. **PDF Compilation (`latex_writer.py`):** The final markdown/text is converted into an IEEE-styled LaTeX document and compiled into a downloadable PDF.

---

## 📦 Modules

| Module | Description |
|--------|-------------|
| 🔍 `fetch_semantic.py` | Fetches academic papers and metadata related to the topic. |
| 🗄️ `rag.py` | Handles document embedding and FAISS vector retrieval. |
| 🕵️‍♂️ `agents.py` | Defines the logic for the Research, Analysis, and Writer agents. |
| ✍️ `generator.py` | Generates section-wise content orchestrating the multi-agent workflow. |
| 📜 `latex_writer.py` | Formats output into an IEEE LaTeX template and compiles the PDF. |
| 💻 `app.py` | The main Streamlit web application providing the user interface. |

---

## 🚀 Installation

Ensure you have Python 3.8+ installed. You will also need LaTeX installed on your system to compile PDFs (e.g., `texlive` or `miktex`).

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/ai-research-paper-generator.git
cd ai-research-paper-generator
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```
*(Make sure `streamlit`, `faiss-cpu`, `sentence-transformers`, `requests`, etc., are in your `requirements.txt`)*

### 3. Setup Ollama (Local LLMs)
Download and install [Ollama](https://ollama.com/). Then, pull the model you plan to use (e.g., `llama3` or `mistral`):
```bash
ollama run llama3
```

---

## 💻 How to Run

After ensuring the Ollama server is running in the background, start the Streamlit interface:

```bash
streamlit run app.py
```

Or, if you prefer running it headless via the terminal:

```bash
python main.py
```

---

## 🎯 Example Usage

1. Open the Streamlit web app in your browser at `http://localhost:8501`.
2. Enter your research topic: *"The Impact of Quantum Computing on Cryptography."*
3. Click **"Generate Paper"**.
4. Monitor the multi-agent pipeline progress in the UI.
5. Once complete, click **"Download PDF"** to receive your fully formatted IEEE-style research paper.

---

## 📂 Project Structure

```text
ai-research-paper-generator/
│
├── app.py                 # Streamlit front-end UI
├── main.py                # Terminal-based execution script
├── agents.py              # Multi-agent definitions (Research, Analysis, Writer)
├── fetch_semantic.py      # Module to fetch academic data
├── generator.py           # Core logic for paper generation
├── rag.py                 # RAG implementation with FAISS
├── latex_writer.py        # LaTeX formatting and PDF compilation
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

---

## 🔮 Future Improvements

- [ ] **Multi-format Export:** Support for Word (.docx) and Markdown (.md) exports.
- [ ] **Advanced Graph RAG:** Upgrade from traditional vector RAG to Graph RAG for better semantic relationships.
- [ ] **Internet Browsing Agent:** Add an agent that actively scrapes the latest web articles dynamically.
- [ ] **Custom Templates:** Options for APA, MLA, and Harvard citation styles.

---

## 🤝 Contribution

Contributions are always welcome! Whether you are a beginner or an experienced developer, feel free to dive in.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

<div align="center">
  <b>Built with ❤️ using Open Source AI.</b><br>
  If you found this helpful, please consider leaving a ⭐ on this repository!
</div>
