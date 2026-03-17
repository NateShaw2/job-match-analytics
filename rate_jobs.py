from google import genai
from dotenv import load_dotenv
import os
import typing_extensions as typing

class JobRating(typing.TypedDict):
    score: int
    score_reasoning: str
    skills_required: list[str]
    company: str
    job_title: str

load_dotenv()
client = genai.Client(api_key=os.getenv("AI_API_KEY"))

response = client.models.generate_content(
    model="gemini-2.5-flash", contents="Explain how AI works in a few words"
)
print(response.text)