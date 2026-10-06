from llm.chat import chat
from retrieval.retriever import retrieve
from memory.history import get_history, add_message

def ask(question:str, session_id):
    chunks = retrieve(question)

    context = "\n\n".join(chunk["text"] for chunk in chunks)

    history = get_history(session_id)

    answer = chat(
        question=question,
        context=context,
        history=history
    )

    add_message(session_id, "user", question)
    add_message(session_id, "assistant", answer)

    sources = [
        {
            "text": chunk["text"],
        }
        for chunk in chunks
    ]

    return {
        "answer": answer,
        "sources": sources,
    }