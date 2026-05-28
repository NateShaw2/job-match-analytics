from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import json
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

    def _clean_job(self, job:dict) -> str:
        fields = ["job_title", "job_description", "job_is_remote", 
        "job_posted_at", "job_location", "job_benefits", 
        "job_employment_type", "job_salary_string"]

        parts = []
        for field in fields:
            if value := job.get(field):
                parts.append(f"{field.upper()}:\n{value}")
        return "/n/n".join(parts)

    def rate_job(self, job: dict, resume_text: str, preferences="N/A") -> JobRating:
        response = self.client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=f"Rate this job posting: {job}",
            config=types.GenerateContentConfig(
                system_instruction=f"Your resume: {resume_text}\nPreferences: {preferences}",
                response_mime_type="application/json",
                response_schema=JobRating
            )
        )

        return response.text

if __name__ == "__main__":
    with open("test_data/resume_test.txt", "r", encoding="utf-8") as f:
        resume = f.read()
    with open("test_data/test_jobs.json", "r") as f:
        jobs = json.load(f)

    job = jobs["data"][0]

    rater = RateJobs()
    print(rater.rate_job(job, resume))