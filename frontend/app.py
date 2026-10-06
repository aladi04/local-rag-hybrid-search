import uuid

import requests
import streamlit as st

BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="Local RAG Chat", layout="wide",)

def initialize_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "documents" not in st.session_state:
        st.session_state.documents = []
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

def load_documents():
    try:
        response = requests.get(f"{BACKEND_URL}/documents/")
        response.raise_for_status()
        data = response.json()
    except (requests.exceptions.RequestException, ValueError) as e:
        st.error(f"Error loading documents: {e}")
        return []

    if isinstance(data, dict):
        return data.get("documents", [])
    if isinstance(data, list):
        return data

    return []

def upload_pdf(file):
    files = {"file": (file.name, file, "application/pdf")}
    try:
        response = requests.post(f"{BACKEND_URL}/upload/", files=files)
        response.raise_for_status()
        return response.json()
    except (requests.exceptions.RequestException, ValueError) as e:
        st.error(f"Error uploading file: {e}")
        return None

def delete_document(document_id):
    try:
        response = requests.delete(f"{BACKEND_URL}/documents/{document_id}")
        response.raise_for_status()
        return response.json()
    except (requests.exceptions.RequestException, ValueError) as e:
        st.error(f"Error deleting document: {e}")
        return None

def ask_question(question):
    payload = {
        "question": question,
        "session_id": st.session_state.session_id
    }
    try:
        response = requests.post(f"{BACKEND_URL}/chat/", json=payload)
        response.raise_for_status()
        return response.json()
    except (requests.exceptions.RequestException, ValueError) as e:
        st.error(f"Error asking question: {e}")
        return None

def render_sidebar():
    st.sidebar.title("Local RAG Chat")
    st.sidebar.markdown("Upload PDFs and ask questions based on their content.")

    uploaded_file = st.sidebar.file_uploader("Upload a PDF", type=["pdf"])
    if uploaded_file:
        if st.button("Upload", use_container_width=True):
            with st.spinner("Uploading..."):
                try:
                    upload_pdf(uploaded_file)
                    st.toast(f"{uploaded_file.name} uploaded successfully!", icon="✅")
                    st.session_state.documents = load_documents()
                    st.rerun()
                except Exception as e:
                    st.error(f"Error uploading file: {e}")

    st.divider()
    st.sidebar.subheader("Indexed Documents")
    if not st.session_state.documents:
        st.caption("No documents indexed yet, upload a PDF to get started.")
    else:
        for doc in st.session_state.documents:
            col1, col2 = st.sidebar.columns([4, 1])
            col1.write(doc.get("filename", "Unknown"))
            if col2.button("Delete", key=f"delete_{doc['document_id']}", help="Delete this document"):
                try:
                    delete_document(doc["document_id"])
                    st.session_state.documents = load_documents()
                    st.rerun()
                except Exception as e:
                    st.error(f"Error deleting document: {e}")

    st.divider()

    if st.button("New Chat", use_container_width=True):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.rerun()

def render_chat():
    st.title("Local RAG Chat")
    st.caption("Ask questions based on the content of your uploaded PDFs.")

    if not st.session_state.messages:
        st.info("Start by asking a question in the input box below.")
        st.markdown(
            "Try asking questions like:\n"
            "- What is the main topic of the document?\n"
            "- Summarize the key points.\n"
            "- What are the conclusions or recommendations?\n"
            "- Provide a brief overview of the ..."
        )

    # This should NOT be inside the if
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            if message["role"] == "assistant" and message.get("sources"):
                for source in message["sources"]:
                    label = source.get("filename", "Source")
                    with st.expander(label):
                        st.write(source.get("text", "No content available."))

    # This should also NOT be inside the if
    if question := st.chat_input("Ask a question..."):
        st.session_state.messages.append(
            {"role": "user", "content": question}
        )

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            placeholder = st.empty()

            with st.spinner("Generating response..."):
                result = ask_question(question)
                if result is not None:
                    answer = result.get("answer", "")
                    sources = result.get("sources", [])
                else:
                    answer = "Error: Could not get a response from the backend"
                    sources = []

                placeholder.markdown(answer)

                if sources:
                    for source in sources:
                        label = source.get("filename", "Source")
                        with st.expander(label):
                            st.write(source.get("text", ""))

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
                "sources": sources
            }
        )

def main():
    initialize_state()
    st.session_state.documents = load_documents()
    render_sidebar()
    render_chat()
    st.divider()
    st.caption("Powered by Streamlit, FastAPI, Qdrant, Ollama")

if __name__ == "__main__":
    main()