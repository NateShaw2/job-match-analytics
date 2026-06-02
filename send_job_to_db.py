import pyodbc
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

def get_connection():
    conn = pyodbc.connect(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={os.getenv('DB_SERVER')};"
        f"DATABASE={os.getenv('DB_DATABASE')};"
        f"Trusted_Connection=yes;"
    )
    return conn

def insert_resume(resume_text: str) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("{CALL usp_insert_resume(?)}", resume_text)
    row = cursor.fetchone()
    conn.commit()
    conn.close()
    return row[0]

def insert_job(job: dict, rating: dict, resume_id: int, query_search: str):
    conn = get_connection()
    cursor = conn.cursor()

    params = {
        "job_id": job.get("job_id"),
        "job_title": job.get("job_title"),
        "employer_name": job.get("employer_name"),
        "employer_website": job.get("employer_website"),
        "job_publisher": job.get("job_publisher"),
        "job_employment_type": job.get("job_employment_type"),
        "job_description": job.get("job_description"),
        "job_posted_at": job.get("job_posted_at"),
        "job_posted_at_datetime_utc": job.get("job_posted_at_datetime_utc"),
        "job_rated_at": datetime.utcnow(),
        "job_location": job.get("job_location"),
        "job_city": job.get("job_city"),
        "job_state": job.get("job_state"),
        "job_country": job.get("job_country"),
        "job_benefits": job.get("job_benefits"),
        "job_salary_string": job.get("job_salary_string"),
        "job_min_salary": job.get("job_min_salary"),
        "job_max_salary": job.get("job_max_salary"),
        "job_salary_period": job.get("job_salary_period"),
        "job_score": rating.get("score"),
        "job_score_reasoning": rating.get("score_reasoning"),
        "job_skills_required": rating.get("skills_required"),
        "job_posting_quality_score": rating.get("posting_quality_score"),
        "job_posting_quality_score_reasoning": rating.get("posting_quality_score_reasoning"),
        "job_query_search": query_search,
        "resume_id": resume_id,
        "query_keywords": ",".join(query_search.split()),
        "title_words": ",".join(job.get("job_title", "").split()),
    }

    placeholders = ", ".join(["?"] * len(params))
    cursor.execute(f"{{CALL usp_insert_job({placeholders})}}", list(params.values()))
    conn.commit()
    conn.close()

def main():
    resume_text = "Experienced data analyst with SQL Server, Power BI, and Python skills."

    job = {
        "job_id": "279NCBNmAadGOWIMAAAAAA==",
        "job_title": "Financial Data Analyst - Population Health",
        "employer_name": "The Vancouver Clinic",
        "employer_website": None,
        "job_publisher": "Indeed",
        "job_employment_type": "Full-time",
        "job_description": "The Population Health Financial Data Analyst will support clinic operations...",
        "job_posted_at": "5 days ago",
        "job_posted_at_datetime_utc": datetime.strptime("2026-04-02T00:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ"),
        "job_location": "Vancouver, WA",
        "job_city": "Vancouver",
        "job_state": "Washington",
        "job_country": "US",
        "job_benefits": "health_insurance,dental_coverage",
        "job_salary_string": "$88,037.00 - $132,055.00",
        "job_min_salary": 88037,
        "job_max_salary": 132055,
        "job_salary_period": "YEAR",
    }

    rating = {
        "score": 72,
        "score_reasoning": "Candidate has strong SQL and Power BI experience but lacks healthcare domain knowledge and 5 years minimum experience required.",
        "skills_required": "SQL,Power BI,Excel,Financial Modeling,Healthcare Analytics",
        "posting_quality_score": 85,
        "posting_quality_score_reasoning": "Legitimate posting from a known healthcare organization with detailed requirements and salary range provided.",
    }

    query_search = "junior data analyst"

    resume_id = insert_resume(resume_text)
    print(f"resume_id: {resume_id}")

    insert_job(job, rating, resume_id, query_search)
    print("Job inserted successfully")

if __name__ == "__main__":
    main()