# quizzer/search.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()
SERPER_API_KEY = os.getenv("SERPERDEV_API_KEY")


def search_web(query: str):
    """
    Perform Google-like search using SerperDev API and return top 3 snippet results.
    """
    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
    data = {"q": query}

    try:
        res = requests.post(url, headers=headers, json=data)
        results = res.json().get("organic", [])[:3]
        snippets = [r.get("snippet", "") for r in results]
        return "\n".join(snippets)
    except Exception as e:
        return "Web search failed."
