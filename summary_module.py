from google import genai
from google.genai import errors
import os
import time
from dotenv import load_dotenv
from google.genai.errors import ServerError, ClientError

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def summarize(text):
    prompt = f"Summarize this in 5 simple points:\n{text}"

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )
            return response.text

        except errors.ServerError:
            if attempt < 2:
                time.sleep(2 ** attempt)
            else:
                return "Gemini server is busy (503). Please try again."

        except Exception as e:
            return f"Error: {e}"