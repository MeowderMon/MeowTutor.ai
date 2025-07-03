# chatbot/chatbot.py
import os
import streamlit as st
from langchain.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings,ChatGoogleGenerativeAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory


def _missing_api_key() -> bool:
    return not os.getenv("GOOGLE_API_KEY", "").strip()


def create_chatbot_chain(documents):
    """
    Build a ConversationalRetrievalChain from a list of LangChain Documents.
    Returns the chain or raises a ValueError with a user-readable message.
    """

    # ---------- 1. Basic validations ----------
    if _missing_api_key():
        raise ValueError(
            "GOOGLE_API_KEY is not set. Add it to your .env or Streamlit secrets."
        )

    if not documents:
        raise ValueError(
            "No text was extracted from the PDF, so the AI Tutor cannot be initialised."
        )

    # ---------- 2. Build components ----------
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
    )

    vector_store = FAISS.from_documents(documents, embeddings)

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.3,
        google_api_key=os.getenv("GOOGLE_API_KEY"),
    )

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        output_key="answer",
        return_messages=True,
    )

    # ---------- 3. Assemble chain ----------
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
        memory=memory,
        return_source_documents=True,
    )
    return chain
