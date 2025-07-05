import json, re, os, streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema      import SystemMessage, HumanMessage


# ── helper: strip ```
def _clean_json(raw: str) -> str:
    txt = raw.strip()

    # remove markdown fences if present
    if txt.startswith("```"):
        txt = re.sub(r"^``````$", "", txt, flags=re.IGNORECASE | re.DOTALL).strip()

    # some models prepend text → keep only the first {...}
    start = txt.find("{")
    end   = txt.rfind("}")
    if start != -1 and end != -1:
        txt = txt[start : end + 1]

    return txt


def _parse_llm_json(raw: str) -> dict:
    clean = _clean_json(raw)
    try:
        return json.loads(clean)
    except json.JSONDecodeError as e:
        raise ValueError(f"❌ Model returned invalid JSON\n\n-----\n{raw}\n-----") from e


# ────────────────────────────────────────────────────────────────
def generate_quiz(text: str, num_q: int = 10, difficulty: str = "Medium") -> dict:
    """
    Ask Gemini to create MCQs and return them as a Python dict.
    Returns  {"questions":[...]}  or  {}  if anything goes wrong.
    """

    api_key = os.getenv("GOOGLE_API_KEY", "")
    if not api_key:
        st.error("GOOGLE_API_KEY missing.")
        return {}

    llm = ChatGoogleGenerativeAI(
        model       = "gemini-2.5-flash",
        temperature = 0.9,
        google_api_key = api_key,
    )

    sys_prompt = (
        "You are an expert quiz generator.\n"
        f"Create {num_q} multiple-choice questions (difficulty: {difficulty}).\n"
        "Return ONLY valid JSON using this schema:\n"
        "{\n"
        '  "questions": [\n'
        "    {\n"
        '      "question": str,\n'
        '      "options": {"A": str, "B": str, "C": str, "D": str},\n'
        '      "correct_answer": "A" | "B" | "C" | "D",\n'
        '      "explanation": str\n'
        "    }\n"
        "  ]\n"
        "}"
    )

    user_msg = text[:3000]  # token safety
    messages = [SystemMessage(content=sys_prompt), HumanMessage(content=user_msg)]

    # use .invoke (recommended) instead of deprecated __call__
    response = llm.invoke(messages)
    raw_out  = response.content or ""

    try:
        return _parse_llm_json(raw_out)
    except ValueError as e:
        st.error(str(e))
        return {}
