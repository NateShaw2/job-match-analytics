ALTER TABLE job_title_words
ADD CONSTRAINT FK_job_title_words FOREIGN KEY (job_id) REFERENCES jobs(job_id);

ALTER TABLE job_query
ADD CONSTRAINT FK_job_query FOREIGN KEY (job_id) REFERENCES jobs(job_id);