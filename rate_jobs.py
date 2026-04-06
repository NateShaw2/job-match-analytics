from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import typing_extensions as typing

class JobRating(typing.TypedDict):
    score: int
    score_reasoning: str
    skills_required: list[str]
    quality_score: int

class RateJobs:
    def __init__(self):
        load_dotenv()
        self.client = genai.Client(api_key=os.getenv("AI_API_KEY"))

    def rate_job(self, job, resume_text, preferences):
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=f"Rate this job posting: {job}",
        config=types.GenerateContentConfig(
            system_instruction=f"Your resume: {resume_text}\nPreferences: {preferences}",
            response_mime_type="application/json",
            response_schema=JobRating
        )
    )

    return response.text