import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY is missing. Check your .env file."
    )

client = genai.Client(api_key=api_key)


def ask_gemini(prompt: str) -> str:
    """Send a prompt to Gemini and return its response."""

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt,
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty response.")

    return response.text
