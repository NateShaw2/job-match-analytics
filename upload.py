import json
import os
import argparse
import time
from datetime import datetime
from resume_loader import load_resume
from rate_jobs import RateJobs
from send_job_to_db import insert_resume, insert_job

DEBUG = True

def upload(filename: str):
    with open(filename, "r") as f:
        jobs = json.load(f)
    print(f"Loaded {len(jobs)} jobs from {filename}")

    resume_text = load_resume("resume.txt")
    resume_id = insert_resume(resume_text)
    print(f"Resume loaded with resume_id: {resume_id}")

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

    # Rename file on success
    base, ext = os.path.splitext(filename)
    renamed = f"{base}_uploaded{ext}"
    os.rename(filename, renamed)
    print(f"\nUpload complete. File renamed to {renamed}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Path to the JSON file to upload")
    args = parser.parse_args()
    upload(args.file)