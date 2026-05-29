import pytest
from unittest.mock import patch, Mock
from retrieve_jobs import GetJobs

class TestFetchMethods:
	def test_fetch(self):
		jobs = GetJobs()
		assert(len(jobs._fetch(search_terms="data analyst", page_number=1, results_per_page=1)) == 1)

	def test_fetch_jobs(self):
		jobs = GetJobs(search_terms=["data analyst"])
		assert(len(jobs.fetch_jobs(pages=1, results_per_page=1)) == 1)	


class TestErrorHandling:
	def test_invalid_fetch_response(self):
		with patch('requests.get') as mock_get:
			mock_response = Mock()
			mock_response.json.return_value = {"results": []}
			mock_response.status_code = 200
			mock_get.return_value = mock_response

			jobs = GetJobs()
			assert(len(jobs._fetch("data analyst", page_number=1)) == 0)

	def test_no_id(self):
		with patch('requests.get') as mock_get:
			mock_response = Mock()
			mock_response.json.return_value = {
				"results": [{"title": "Job without ID"}, 
				{"id": 132, "title": "data analyst"}]
			}

			mock_get.return_value = mock_response

			jobs = GetJobs(search_terms=["data analyst"])
			assert(len(jobs.fetch_jobs(pages=1, results_per_page=1)) == 1)