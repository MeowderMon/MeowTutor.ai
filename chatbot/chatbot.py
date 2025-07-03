import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

load_dotenv()

gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

def generate_chatbot_response(query: str, context: str) -> str:
    """
    Uses Gemini via LangChain to answer user queries based on the document context.
    """
    prompt_template = (
        "You are a helpful tutor. Use the following context to answer the student's question.\n"
        "\nContext:\n{context}\n"
        "\nQuestion: {question}\n"
        "Answer:"
    )
    prompt = PromptTemplate(input_variables=["context", "question"], template=prompt_template)
    chain = LLMChain(llm=gemini_llm, prompt=prompt)
    return chain.run({"context": context, "question": query})
