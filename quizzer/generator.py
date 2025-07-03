import os
import json
from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

llm = GoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key)

def generate_mcqs_from_text(text, num_questions=5):
    prompt = f"""
You are a quiz generator. Based on the content below, generate {num_questions} multiple choice questions.
Each question should have 4 options and one correct answer, and a brief explanation for the answer.

Return the result strictly in JSON format inside triple backticks like this:

\\`\\`\\`json
[
  {{
    "question": "What is the capital of France?",
    "options": ["Paris", "Berlin", "Rome", "Madrid"],
    "answer": "Paris"
    "explanation":"Because Paris has been the seat of the French government since the Middle Ages."
  }}
]
\\`\\`\\`

CONTENT:
{text[:3000]}
"""

    try:
        response = llm.invoke(prompt)
        if "```" in response:
            parts = response.split("```")
            json_block = parts[1]
            if json_block.strip().lower().startswith("json"):
                json_block = "\n".join(json_block.splitlines()[1:])
            json_code = json_block.strip()
        else:
            json_code = response.strip()

        result = json.loads(json_code)

        if isinstance(result, list):
            return result
        return []
    except Exception:
        return []
