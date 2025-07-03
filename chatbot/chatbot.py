# chatbot/chatbot.py  (full file)
import os, streamlit as st
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings,
)
from langchain_community.vectorstores import FAISS          # ← new import path
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory


def create_chatbot_chain(documents):
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY env var not set")

    # embeddings
    embed_model = GoogleGenerativeAIEmbeddings(
        google_api_key=api_key, model="models/embedding-001"
    )

    vectordb = FAISS.from_documents(documents, embed_model)

    llm = ChatGoogleGenerativeAI(          # temperature now 0-1 range
        google_api_key=api_key,
        model="gemini-pro",
        temperature=0.3,
    )

    memory = ConversationBufferMemory(
        return_messages=True,
        memory_key="chat_history",
        output_key="answer",
    )

    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectordb.as_retriever(search_kwargs={"k": 3}),
        memory=memory,
        return_source_documents=True,
    )
