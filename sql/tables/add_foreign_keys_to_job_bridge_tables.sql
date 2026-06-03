ALTER TABLE job_title
ADD CONSTRAINT FK_job_title FOREIGN KEY (job_id) REFERENCES jobs(job_id);

ALTER TABLE job_query
ADD CONSTRAINT FK_job_query FOREIGN KEY (job_id) REFERENCES jobs(job_id);