import os
import time

from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise Exception("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=API_KEY)

# This model already worked for you
MODEL_NAME = "gemini-3-flash-preview"


def ask_gemini(prompt: str):

    for attempt in range(5):

        try:

            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )

            return response.text

        except Exception as e:

            error = str(e)

            # Retry only for temporary server overloads
            if "503" in error or "UNAVAILABLE" in error:

                wait = 2 ** attempt

                print(f"Gemini busy... retrying in {wait} seconds")

                time.sleep(wait)

                continue

            # Any other error should be raised immediately
            raise

    raise Exception("Gemini is temporarily unavailable. Please try again later.")


if __name__ == "__main__":

    print("Testing Gemini...\n")

    answer = ask_gemini(
        "Reply with exactly one word: Success"
    )

    print(answer)