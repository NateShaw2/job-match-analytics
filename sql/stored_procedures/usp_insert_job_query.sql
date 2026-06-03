-- =============================================
-- Create date: 6/2/2026
-- Description: Inserts job query data
-- =============================================
CREATE OR ALTER PROCEDURE usp_insert_job_query
    @jobId VARCHAR(255),
    @query VARCHAR(255)
AS
BEGIN
    SET NOCOUNT ON;
	IF NOT EXISTS (SELECT 1 FROM job_query WHERE job_id = @jobId AND job_query = @query)
    INSERT INTO job_query (job_id, job_query)
    VALUES (@jobId, @query)
END
GO