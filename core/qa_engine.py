# core/qa_engine.py
from core.config import client

SYSTEM_PROMPT = """
You are a highly accurate document assistant.
Answer the user's question ONLY using the provided context.
If the answer is not explicitly contained in the context, politely state:
"I cannot find that information in the document."
Do not attempt to guess or use outside knowledge.
"""

def generate_answer(question: str, context_chunks: list, model: str = "gpt-4o-mini") -> str:
    """Generates an answer grounded purely in the retrieved context."""
    if not context_chunks:
        return "No document context available to answer the question."

    context_text = "\n\n---\n\n".join(context_chunks)
    
    response = client.chat.completions.create(
        model=model,
        temperature=0.0, # Set to 0 to minimize hallucinations
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT.strip()},
            {"role": "user", "content": f"Context:\n{context_text}\n\nQuestion:\n{question}"}
        ]
    )

    return response.choices[0].message.content.strip()