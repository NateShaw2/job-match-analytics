CREATE TABLE job_query (
	job_id VARCHAR(255),
	job_query VARCHAR(255),
	CONSTRAINT PK_job_query PRIMARY KEY(job_id, job_query)
)

CREATE TABLE job_title (
	job_id VARCHAR(255),
	job_title VARCHAR(255),
	CONSTRAINT PK_job_title_words PRIMARY KEY(job_id, job_title)
)