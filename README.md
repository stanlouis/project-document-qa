# 📄 Smart Document Q&A App

An AI-powered Retrieval-Augmented Generation (RAG) application that allows users to upload documents and ask natural language questions about their contents.

This project is specifically designed to **eliminate LLM hallucinations** by forcing the model to strictly cite its sources from the uploaded context. It features a persistent local vector database, meaning you can index multiple documents over time and query across all of them without needing to re-upload files.

## ✨ Features

* **Multi-Format Support:** Extracts text seamlessly from both `.txt` and `.pdf` files (powered by PyMuPDF).
* **Persistent Vector Storage:** Uses ChromaDB to save document embeddings locally, allowing you to maintain a persistent knowledge base across application restarts.
* **Strict Grounding:** Utilizes a highly constrained prompt engine with a `0.0` temperature setting to ensure the AI answers *only* using the provided document context.
* **Interactive UI:** A clean, two-column Gradio web interface for easy uploading, indexing, and querying.

## 🛠️ Tech Stack

* **Language:** Python 3.8+
* **LLM & Embeddings:** OpenAI API (`gpt-4o-mini`, `text-embedding-3-small`)
* **Vector Database:** ChromaDB
* **Document Parsing:** PyMuPDF (`fitz`), Tiktoken
* **Frontend:** Gradio

## 🚀 Setup & Installation

**1. Clone the repository**

```bash
git clone [https://github.com/stanlouis/project-document-qa.git](https://github.com/stanlouis/project-document-qa.git)
cd project-document-qa
```

**2. Create and activate a virtual environment**

```bash
# Mac/Linux
python -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Configure Environment Variables**
Create a `.env` file in the root directory and add your OpenAI API key:

```text
OPENAI_API_KEY=your_api_key_here
```

*(Note: Do not commit your `.env` file to version control. It is ignored in `.gitignore` by default).*

## 💻 Usage

Start the Gradio application by running:

```bash
python app.py
```

The application will launch a local web server (usually at `http://127.0.0.1:7860/`).

**Workflow:**

1. Upload a `.txt` or `.pdf` file.
2. Click **Index Document** to extract, chunk, and save the text to the local ChromaDB database.
3. Type a question in the query box and click **Submit Question**.
4. *(Optional)* Click **Clear Database** if you want to wipe the local vector store and start fresh.

## � Cloud vs. Local Execution

This project supports two distinct operational modes, each managed on its own Git branch, so you can switch between them cleanly without touching any code.

| | Cloud Mode (OpenAI) | Local Mode (Ollama) |
|---|---|---|
| **Branch** | `main` | `feature/local-ollama` |
| **LLM** | `gpt-4o-mini` | `llama3.2` |
| **Embeddings** | `text-embedding-3-small` | `nomic-embed-text` |
| **Cost** | Pay-per-token | Free |
| **Privacy** | Data sent to OpenAI | 100% local |
| **Vector DB** | `chroma_data/` | `chroma_data_ollama/` |

### ☁️ Cloud Mode (OpenAI)

The `main` branch uses OpenAI's hosted models. It requires a valid API key and sends your document chunks to OpenAI's servers for embedding and inference.

```bash
git switch main
```

Ensure your `.env` file contains:
```text
OPENAI_API_KEY=your_api_key_here
```

### 🏠 Local Mode (Ollama)

The `feature/local-ollama` branch runs entirely on your own machine — no API key, no cost, and no data leaves your device.

```bash
git switch feature/local-ollama
```

**Prerequisites:** Before running this branch, install [Ollama](https://ollama.com) and pull the required models:

```bash
ollama pull llama3.2
ollama pull nomic-embed-text
```

### ⚠️ Database Isolation

The two branches use **separate vector databases** (`chroma_data/` vs `chroma_data_ollama/`). This is intentional: `text-embedding-3-small` produces 1536-dimensional vectors while `nomic-embed-text` produces 768-dimensional vectors, so the databases are fundamentally incompatible. Documents indexed in one branch will **not** appear when querying from the other. You will need to re-index your documents after switching branches.

---

## �📂 Project Architecture

```text
project-document-qa/
├── app.py                 # Gradio user interface and event routing
├── requirements.txt       # Project dependencies
├── .env                   # Environment variables (not tracked)
├── .gitignore             # Git exclusion rules
├── chroma_data/           # Auto-generated persistent vector database (not tracked)
└── core/                  # Encapsulated backend logic
    ├── config.py          # Centralized configuration and API setup
    ├── chunker.py         # Token-based text splitting and PDF extraction
    ├── embeddings.py      # OpenAI embedding generation
    ├── vector_store.py    # Persistent ChromaDB management
    └── qa_engine.py       # Prompting and LLM interaction
```

```

***

