import ollama

MODEL = "llama3.2"

def chat(question: str, context: str, history: str):
    prompt = f"""
You are a helpful assistant. 
Answer Only based on the context provided.

Context: {context}
Question: {question}
History: {history}
"""

    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt,}],
    )

    return response["message"]["content"]