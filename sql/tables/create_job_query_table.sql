CREATE TABLE job_query (
	job_id VARCHAR(255),
	job_query VARCHAR(255),
	CONSTRAINT PK_job_query PRIMARY KEY(job_id, job_query)
)

ALTER TABLE job_query
ADD CONSTRAINT FK_job_query FOREIGN KEY (job_id) REFERENCES jobs(job_id);