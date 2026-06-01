-- =============================================
-- Create date: 6/1/2026
-- Description:	If resume data does not exist, then insert into resume. Returns resume_id of resume data.
-- =============================================
CREATE PROCEDURE usp_insert_resume 
	-- Add the parameters for the stored procedure here
	@resume_text VARCHAR(MAX) 
AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;

    INSERT INTO resumes (resume_text, date_inserted)
	SELECT @resume_text, GETDATE()
	WHERE NOT EXISTS (SELECT 1 FROM resumes WHERE resume_hash = HASHBYTES('SHA2_256', @resume_text));

	SELECT resume_id FROM resumes WHERE resume_hash = HASHBYTES('SHA2_256', @resume_text);
END
GO