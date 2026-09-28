import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import errors
from google.genai.errors import ServerError, ClientError

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def explain(topic):
    prompt = f"Explain {topic} in simple English for students. No markdown."

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )
            return response.text

        except errors.ServerError:
            if attempt < 2:
                time.sleep(2 ** attempt)   # 1s, 2s
            else:
                return "Gemini server is busy (503). Please try again in a few seconds."

        except Exception as e:
            return f"Error: {e}"