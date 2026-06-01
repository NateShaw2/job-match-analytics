ALTER TABLE job_title_words
ADD CONSTRAINT FK_job_title_words FOREIGN KEY (job_id) REFERENCES jobs(job_id);

ALTER TABLE job_query_keywords
ADD CONSTRAINT FK_job_query_keywords FOREIGN KEY (job_id) REFERENCES jobs(job_id);