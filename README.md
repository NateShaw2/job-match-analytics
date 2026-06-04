# job-match-analytics

An automated data pipeline that fetches job postings via API, analyzes resume-job fit using AI, and visualizes insights through a Power BI dashboard. Built to demonstrate end-to-end data engineering and analytics skills.

## Overview

1. Job postings are fetched from the JSearch API via RapidAPI
2. Each posting is rated against your resume using the Gemini AI model
3. Results are stored in a local SQL Server database
4. A Power BI dashboard visualizes job fit scores, query performance, and posting quality

## Prerequisites

- Python 3.10+
- SQL Server (local instance with Windows Authentication)
- ODBC Driver 17 for SQL Server
- Power BI Desktop
- RapidAPI account with JSearch subscription (this is the primary limiting factor on the free tier)
- Google AI Studio account for Gemini API access

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/NateShaw2/job-match-analytics.git
cd job-match-analytics
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory:

```
# --- Job Source API ---
RAPIDAPI_HOST=
RAPIDAPI_KEY=
BASE_URL=

# --- AI Rating API ---
AI_API_KEY=

# --- Database ---
DB_SERVER=
DB_DATABASE=
```

- `RAPIDAPI_HOST` — set to `jsearch.p.rapidapi.com`
- `RAPIDAPI_KEY` — your RapidAPI key (see [Getting API Keys](#getting-api-keys))
- `BASE_URL` — set to `https://jsearch.p.rapidapi.com/search-v2`. If you use a different endpoint the response field names will need to be updated throughout `retrieve_jobs.py`, `send_job_to_db.py`, and the stored procedures
- `AI_API_KEY` — your Gemini API key (see [Getting API Keys](#getting-api-keys))
- `DB_SERVER` — your SQL Server instance name (e.g. `localhost` or `.\SQLEXPRESS`)
- `DB_DATABASE` — the name of your database

### 4. Set Up the Database

Run the SQL scripts in the following order in SQL Server Management Studio (SSMS) or Azure Data Studio:

**Tables:**
1. `sql/tables/create_jobs_table.sql`
2. `sql/tables/create_resumes_table.sql`
3. `sql/tables/create_job_query_table.sql`

Note: `jobs.sql` must be run before `resumes.sql` as `resumes.sql` contains an ALTER statement that adds a foreign key constraint on the jobs table.

**Stored Procedures:**
1. `sql/stored_procedures/usp_insert_resume.sql`
2. `sql/stored_procedures/usp_insert_job.sql`
3. `sql/stored_procedures/usp_insert_job_query.sql`

### 5. Add Your Resume

Place your resume as a plain text file named `resume.txt` in the root directory.

### 6. Configure Search Queries and Model

The job search queries and AI model are hardcoded in `main.py`:

```python
param_list = [
    {"query": "Data Analyst", "num_pages": "1", "country": "us", "date_posted": "3days"},
    {"query": "Business Analyst", "num_pages": "1", "country": "us", "date_posted": "3days"},
    {"query": "Reporting Analyst", "num_pages": "1", "country": "us", "date_posted": "3days"},
]
```

Update these to match the roles you are targeting. The Gemini model is hardcoded in `rate_jobs.py` — update `model_name` there if you want to use a different model.

## Running the Pipeline

### Normal Run (fetch, rate, and insert to database)

```bash
python main.py
```

### Save Run (fetch only, save to JSON file, skip rating and database insert)

```bash
python main.py --save
```

This saves jobs to a timestamped file like `jobs_20260602_143022.json`. Useful when the database is unavailable or you want to preserve API results before rating.

### Upload from Saved File

```bash
python upload.py jobs_20260602_143022.json
```

This loads the saved JSON, rates each job via Gemini, inserts to the database, and renames the file to `jobs_20260602_143022_uploaded.json` on completion.

## Power BI Dashboard

### Connecting to Your Database

1. Open `Job_Analytics_Template.pbix` in Power BI Desktop
2. Go to **Transform Data → Data Source Settings**
3. Update the server and database name to match your `.env` values
4. Click **Close** and hit **Refresh**

The dashboard expects the following tables: `jobs`, `job_query`, `resumes`

## Getting API Keys

### JSearch (RapidAPI)

1. Create an account at [rapidapi.com](https://rapidapi.com)
2. Search for **JSearch** and subscribe (free tier available)
3. Copy your API key from the RapidAPI dashboard into `RAPIDAPI_KEY`
4. Set `RAPIDAPI_HOST` to `jsearch.p.rapidapi.com`

Note: JSearch is the primary rate limiting factor on the free tier. If you hit limits, use `python main.py --save` to preserve your fetched jobs and upload later via `upload.py`.

### Gemini (Google AI Studio)

1. Go to [aistudio.google.com](https://aistudio.google.com)
2. Click **Get API key** and create a new key
3. Copy it into `AI_API_KEY`

Note: If you hit Gemini rate limits mid-run, increase the `time.sleep()` delay in `main.py` and `upload.py`.

## Project Structure

```
job-match-analytics/
├── main.py                      # Pipeline orchestrator
├── upload.py                    # Upload saved JSON to database
├── resume_loader.py             # Loads resume text from file
├── retrieve_jobs.py             # Fetches jobs from JSearch API
├── rate_jobs.py                 # Rates jobs using Gemini AI
├── send_job_to_db.py            # SQL Server database writes
├── test_get_jobs.py             # Tests for retrieve_jobs.py
├── resume.txt                   # Your resume (not tracked in git)
├── .env                         # Environment variables (not tracked in git)
├── Job_Analytics_Template.pbix  # Power BI dashboard template
└── sql/
    ├── tables/
    │   ├── create_resumes_table.sql
    │   ├── create_jobs_table.sql
    │   └── create_job_query_table.sql
    └── stored_procedures/
        ├── usp_insert_resume.sql
        ├── usp_insert_job.sql
        └── usp_insert_job_query.sql
```