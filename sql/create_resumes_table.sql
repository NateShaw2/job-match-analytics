CREATE TABLE resumes (
	resume_id INT PRIMARY KEY,
	resume_text VARCHAR(MAX),
	date_inserted DATETIME
);

ALTER TABLE jobs
ADD CONSTRAINT FK_jobs_resume FOREIGN KEY (resume_id) REFERENCES resumes(resume_id);