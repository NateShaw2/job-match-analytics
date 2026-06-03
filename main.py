import os
from datetime import datetime
from dotenv import load_dotenv
from resume_loader import load_resume
from retrieve_jobs import GetJobs
from rate_jobs import RateJobs
from send_job_to_db import insert_resume, insert_job

load_dotenv()

DEBUG = True

def main():
    # Load resume
    resume_text = load_resume("resume.txt")
    resume_id = insert_resume(resume_text)
    print(f"Resume loaded with resume_id: {resume_id}")

    # API setup
    host = os.getenv("RAPIDAPI_HOST")
    key = os.getenv("RAPIDAPI_KEY")
    base_url = os.getenv("BASE_URL")
    headers = {
        "x-rapidapi-key": key,
        "x-rapidapi-host": host,
        "Content-Type": "application/json"
    }

    param_list = [
        {"query": "Junior Data Analyst near Vancouver, Washington", "num_pages": "1", "country": "us", "date_posted": "week"},
        {"query": "Business Analyst near Vancouver Washington", "num_pages": "1", "country": "us", "date_posted": "week"},
        {"query": "Reporting Analyst near Vancouver Washington", "num_pages": "1", "country": "us", "date_posted": "week"},
    ]

    # Fetch jobs
    fetcher = GetJobs()
    jobs = fetcher.fetch_jobs(base_url, headers, param_list)
    print(f"Total unique jobs fetched: {len(jobs)}")

    # Rate and insert jobs
    rater = RateJobs(resume_text)
    for job_id, job in jobs.items():
        if DEBUG:
            print(f"\nRating job: {job.get('job_title')} at {job.get('employer_name')}")

        # Data prep before passing to db
        if isinstance(job.get("job_benefits"), list):
            job["job_benefits"] = ",".join(job["job_benefits"])
        if job.get("job_posted_at_datetime_utc"):
            try:
                job["job_posted_at_datetime_utc"] = datetime.strptime(
                    job["job_posted_at_datetime_utc"], "%Y-%m-%dT%H:%M:%S.%fZ"
                )
            except ValueError:
                job["job_posted_at_datetime_utc"] = None

        # Rate job
        rating = rater.rate_job(job)
        if DEBUG:
            print(f"Score: {rating['score']} | Quality: {rating['posting_quality_score']}")
            print(f"Score reasoning: {rating['score_reasoning']}")
            print(f"Skills required: {rating['skills_required']}")
            print(f"Quality reasoning: {rating['posting_quality_score_reasoning']}")

        # Insert to DB
        insert_job(job, rating, resume_id)
        if DEBUG:
            print(f"Inserted job_id: {job_id}")

    print("\nPipeline complete")

if __name__ == "__main__":
    main()