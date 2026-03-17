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

## 📂 Project Architecture

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

