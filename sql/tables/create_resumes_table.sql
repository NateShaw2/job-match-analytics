CREATE TABLE resumes (
	resume_id INT PRIMARY KEY,
	resume_text VARCHAR(MAX),
	resume_hash AS HASHBYTES('SHA_256', resume_text) PERSISTED,
	date_inserted DATETIME
);

ALTER TABLE jobs
ADD CONSTRAINT FK_jobs_resume FOREIGN KEY (resume_id) REFERENCES resumes(resume_id);