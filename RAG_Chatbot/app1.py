import streamlit as st
import tempfile

from langchain_classic.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


st.set_page_config(page_title="PDF RAG Chatbot", layout="wide")
st.title("📄 RAG Chatbot (Local Ollama)")


# ------------------ CACHE HEAVY OBJECTS ------------------

@st.cache_resource
def load_embeddings():
    return HuggingFaceEmbeddings(
        model_name="nomic-ai/nomic-embed-text-v1",
        model_kwargs={"trust_remote_code": True}
    )

@st.cache_resource
def load_llm(model_name):
    return OllamaLLM(model=model_name, temperature=0)

# ------------------ PDF PROCESSING ------------------

def process_pdf(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        loader = PyPDFLoader(tmp.name)
        
        # Load only first 20 pages to save resources
        docs = loader.load()[:20]

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,     # smaller chunks = faster
        chunk_overlap=100
    )
    chunks = splitter.split_documents(docs)

    vectorstore = FAISS.from_documents(chunks, embeddings)
    return vectorstore


# ------------------ SIDEBAR ------------------

with st.sidebar:
    st.subheader("Model")
    model_name = st.selectbox("Choose LLM", ["mistral"])

    st.info("Make sure Ollama is running:\n\n`ollama serve`")


# ------------------ MAIN APP ------------------

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file:
    with st.spinner("Processing PDF..."):
        embeddings = load_embeddings()
        vectorstore = process_pdf(uploaded_file)

    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    llm = load_llm(model_name)

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        return_source_documents=False
    )

    st.success("PDF processed successfully!")

    # ---------- Suggested Questions ----------
    st.subheader("💡 Suggested questions")

    questions = [
        "List all chapter names",
        "Give a short summary of the first chapter",
        "What is the chapter about Dolphins?",
        "List important topics covered in this book",
        "Give 5 important exam questions from the Dolphins chapter"
    ]

    for q in questions:
        if st.button(q):
            with st.spinner("Thinking..."):
                answer = qa_chain.run(q)
            st.write("### Answer")
            st.write(answer)

    # ---------- User Question ----------
    user_question = st.text_input("Ask about the PDF")

    if user_question:
        with st.spinner("Thinking..."):
            response = qa_chain.run(user_question)

        st.write("### Answer")
        st.write(response)
