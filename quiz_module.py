import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai.errors import ServerError, ClientError

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_quiz(topic):
    prompt = f"""
Create ONE multiple choice quiz for the topic: {topic}.

Format exactly like this:

Question: ...
A. ...
B. ...
C. ...
Answer: A
"""

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )
            return response.text

        except ServerError:
            # Handles temporary 503 errors
            if attempt < 2:
                time.sleep(2 ** attempt)
            else:
                return "Gemini server is busy. Please try again."

        except ClientError as e:
            # Handles 429 quota exceeded
            if "RESOURCE_EXHAUSTED" in str(e):
                return "Free Gemini quota exceeded. Please wait about 30–60 seconds and try again."
            return f"Client Error: {e}"

        except Exception as e:
            return f"Error: {e}"