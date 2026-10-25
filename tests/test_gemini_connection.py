
import time

from google.genai.errors import ServerError

from app.gemini_client import ask_gemini


def test_gemini_returns_a_response():
    response = None

    for attempt in range(3):
        try:
            response = ask_gemini(
                "Reply with exactly: Gemini connection successful"
            )
            break

        except ServerError as error:
            if error.code not in (500, 502, 503, 504):
                raise

            if attempt == 2:
                raise

            print(
                f"\nTemporary Gemini server error. "
                f"Retrying ({attempt + 1}/2)..."
            )
            time.sleep(2 * (attempt + 1))

    assert isinstance(response, str)
    assert response.strip() != ""

    print("\nGemini response:", response)
