import os
import json
import argparse
from datetime import datetime, timezone
from dotenv import load_dotenv
from resume_loader import load_resume
from retrieve_jobs import GetJobs
from rate_jobs import RateJobs
from send_job_to_db import insert_resume, insert_job
import time

load_dotenv()

DEBUG = True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--save", action="store_true", help="Save jobs to JSON file instead of inserting to DB")
    args = parser.parse_args()

    # Load resume
    resume_text = load_resume("resume.txt")
    if not args.save:
        resume_id = insert_resume(resume_text)
        print(f"Resume loaded with resume_id: {resume_id}")
    else:
        print("Resume loaded")

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
        {"query": "Junior Data Analyst near Vancouver Washington", "num_pages": "1", "country": "us", "date_posted": "3days"},
        {"query": "Business Analyst near Vancouver Washington", "num_pages": "1", "country": "us", "date_posted": "3days"},
        {"query": "Reporting Analyst near Vancouver Washington", "num_pages": "1", "country": "us", "date_posted": "3days"},
    ]

    # Exclude job publishers whose job postings are mostly unhelpful.
    publishers_to_exclude = "Talent.com, Learn4Good"
    for param in param_list:
        param["exclude_job_publishers"] = publishers_to_exclude

    # Fetch jobs
    fetcher = GetJobs()
    jobs = fetcher.fetch_jobs(base_url, headers, param_list)
    print(f"Total unique jobs fetched: {len(jobs)}")

    if args.save:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        filename = f"jobs_{timestamp}.json"
        with open(filename, "w") as f:
            json.dump(jobs, f, indent=2, default=str)
        print(f"Jobs saved to {filename}")
        return

    # Rate and insert jobs
    rater = RateJobs(resume_text)
    for job_id, job in jobs.items():
        if DEBUG:
            print(f"\nRating job: {job.get('job_title')} at {job.get('employer_name')}")

        # Data prep
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

        # Wait 4 seconds to not get rate-limited
        time.sleep(4)

    print("\nPipeline complete")

if __name__ == "__main__":
    main()