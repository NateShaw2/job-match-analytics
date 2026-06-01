CREATE TABLE job_query_keywords (
	job_id VARCHAR(255),
	job_query_keyword VARCHAR(255),
	CONSTRAINT PK_job_query_keywords PRIMARY KEY(job_id, job_query_keyword)
)

CREATE TABLE job_title_words (
	job_id VARCHAR(255),
	job_title_word VARCHAR(255),
	CONSTRAINT PK_job_title_words PRIMARY KEY(job_id, job_title_word)
)