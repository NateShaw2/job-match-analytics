-- =============================================
-- Create date: 6/1/2026
-- Description:	Inserts job data to their respective tables
-- =============================================
CREATE OR ALTER PROCEDURE usp_insert_job
    @job_id VARCHAR(255),
    @job_title VARCHAR(255) = NULL,
    @employer_name VARCHAR(255) = NULL,
    @employer_website VARCHAR(255) = NULL,
    @job_publisher VARCHAR(255) = NULL,
    @job_employment_type VARCHAR(255) = NULL,
    @job_description VARCHAR(MAX),
    @job_posted_at VARCHAR(255) = NULL,
    @job_posted_at_datetime_utc DATETIME = NULL,
    @job_rated_at_utc DATETIME,
    @job_location VARCHAR(255) = NULL,
    @job_city VARCHAR(255) = NULL,
    @job_state VARCHAR(255) = NULL,
    @job_country VARCHAR(255) = NULL,
    @job_benefits VARCHAR(MAX) = NULL,
    @job_salary_string VARCHAR(255) = NULL,
    @job_min_salary INT = NULL,
    @job_max_salary INT = NULL,
    @job_salary_period VARCHAR(255) = NULL,
    @job_score TINYINT,
    @job_score_reasoning VARCHAR(MAX),
    @job_skills_required VARCHAR(MAX),
    @job_posting_quality_score TINYINT,
    @job_posting_quality_score_reasoning VARCHAR(MAX),
	@job_apply_link VARCHAR(255) = NULL,
	@job_rating_model_name VARCHAR(255),
    @resume_id INT
AS
BEGIN
    SET NOCOUNT ON;

    IF NOT EXISTS (SELECT 1 FROM jobs WHERE job_id = @job_id)
    BEGIN
        INSERT INTO jobs (
            job_id,
            job_title,
            employer_name,
            employer_website,
            job_publisher,
            job_employment_type,
            job_description,
            job_posted_at,
            job_posted_at_datetime_utc,
            job_rated_at_utc,
            job_location,
            job_city,
            job_state,
            job_country,
            job_benefits,
            job_salary_string,
            job_min_salary,
            job_max_salary,
            job_salary_period,
            job_score,
            job_score_reasoning,
            job_skills_required,
            job_posting_quality_score,
            job_posting_quality_score_reasoning,
			job_apply_link,
			job_rating_model_name,
            resume_id
        )
        VALUES (
            @job_id,
            @job_title,
            @employer_name,
            @employer_website,
            @job_publisher,
            @job_employment_type,
            @job_description,
            @job_posted_at,
            @job_posted_at_datetime_utc,
            @job_rated_at_utc,
            @job_location,
            @job_city,
            @job_state,
            @job_country,
            @job_benefits,
            @job_salary_string,
            @job_min_salary,
            @job_max_salary,
            @job_salary_period,
            @job_score,
            @job_score_reasoning,
            @job_skills_required,
            @job_posting_quality_score,
            @job_posting_quality_score_reasoning,
			@job_apply_link,
			@job_rating_model_name,
            @resume_id
        );

    END
END
GO