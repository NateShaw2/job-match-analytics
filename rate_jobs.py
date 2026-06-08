from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import json
import typing_extensions as typing
from resume_loader import load_profile

class JobRating(typing.TypedDict):
    score: int = Field(ge=0, le=100)
    score_reasoning: str
    skills_required: list[str]
    posting_quality_score: int = Field(ge=0, le=100)
    posting_quality_score_reasoning: str

class RateJobs:
    def __init__(self, resume_text: str, preferences: str = "N/A"):
        load_dotenv()
        self.client = genai.Client(api_key=os.getenv("AI_API_KEY"))
        applicant_profile = load_profile()
        self.system_prompt = f"""You are a job-fit evaluator. Given a resume and optional preferences,
rate how well the candidate matches the job posting.

Applicant profile:
{applicant_profile}

Resume:
{resume_text}

Score the job from 0 to 100 where:
0 = completely unqualified, no relevant experience
25 = some transferable skills but missing most requirements
50 = partial match but lacking critical requirement(s)
75 = strong match with minor gaps
100 = perfect match, meets all requirements

Posting quality score from 0 to 100 rates how legitimate and well-written the job posting is:
0 = likely scam or spam, vague promises, no real requirements
25 = poorly written, missing key details, suspicious compensation claims
50 = average posting, some details missing but appears legitimate  
75 = clear requirements, realistic expectations, professional tone
100 = detailed, well-written, transparent about role and compensation

Red flags that lower the posting quality score:
- Vague or unrealistic compensation (e.g. 'earn $5000 a week from home')
- No company name or verifiable details
- Excessive exclamation marks or salesy language
- No actual job requirements listed
- Generic copy-paste descriptions"""

    def _clean_job(self, job: dict) -> str:
        fields = ["job_title", "job_description", "job_is_remote", 
        "job_posted_at", "job_location", "job_benefits", 
        "job_employment_type", "job_salary_string"]

        parts = []
        for field in fields:
            if value := job.get(field):
                parts.append(f"{field.upper()}:\n{value}")
        return "\n\n".join(parts)

    def rate_job(self, job: dict, preferences: str = "N/A") -> JobRating:
        model_name = "gemini-3.1-flash-lite"
        response = self.client.models.generate_content(
            model=model_name, 
            contents=f"Rate this job posting: {self.clean_job(job)}",
            config=types.GenerateContentConfig(
                system_instruction=self.system_prompt,
                response_mime_type="application/json",
                response_schema=JobRating
            )
        )

        result = json.loads(response.text)
        result["rating_model_name"] = model_name
        return result

if __name__ == "__main__":
    with open("test_data/resume_test.txt", "r", encoding="utf-8") as f:
        resume = f.read()
    with open("test_data/test_jobs.json", "r") as f:
        jobs = json.load(f)

    job = jobs["data"][0]

    rater = RateJobs(resume)
    print(rater.rate_job(job))