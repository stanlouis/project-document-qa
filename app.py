# app.py
import os
import gradio as gr
from core.chunker import chunk_text, extract_text_from_pdf
from core.vector_store import VectorStore
from core.qa_engine import generate_answer

store = VectorStore()

def process_document(file_obj) -> str:
    if file_obj is None:
        return "No file uploaded."
        
    file_path = file_obj.name
    ext = os.path.splitext(file_path)[1].lower()
    
    try:
        if ext == ".pdf":
            text = extract_text_from_pdf(file_path)
        elif ext == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
        else:
            return f"Unsupported file type: {ext}"
    except Exception as e:
        return f"Failed to process file: {str(e)}"
        
    if not text.strip():
        return "The document appears to be empty."

    chunks = chunk_text(text)
    store.add_texts(chunks)
    
    # We no longer clear the store; we append to it.
    total_docs = store.collection.count()
    return f"Success! Added {len(chunks)} chunks to the database. Total indexed chunks: {total_docs}"

def ask_question(question: str) -> str:
    if not store.has_documents():
        return "Please upload and process a document first."

    top_chunks = store.similarity_search(question, top_k=3)
    return generate_answer(question, top_chunks)

def reset_database() -> str:
    store.clear_database()
    return "Database cleared successfully. You can upload new documents."

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 📄 Smart Document Q&A App\nUpload **.txt** or **.pdf** files. Documents are saved to a persistent database so you can query across multiple files!")
    
    with gr.Row():
        with gr.Column():
            file_upload = gr.File(label="Upload Document", file_types=[".txt", ".pdf"])
            
            with gr.Row():
                load_btn = gr.Button("Index Document", variant="primary")
                clear_btn = gr.Button("Clear Database", variant="stop")
                
            status_box = gr.Textbox(label="System Status", interactive=False)
            
        with gr.Column():
            user_question = gr.Textbox(label="Ask a question", placeholder="What are the key takeaways?")
            ask_btn = gr.Button("Submit Question")
            llm_answer = gr.Textbox(label="AI Answer", lines=6, interactive=False)

    # Event routing
    load_btn.click(fn=process_document, inputs=file_upload, outputs=status_box)
    clear_btn.click(fn=reset_database, inputs=[], outputs=status_box)
    ask_btn.click(fn=ask_question, inputs=user_question, outputs=llm_answer)

if __name__ == "__main__":
    demo.launch()