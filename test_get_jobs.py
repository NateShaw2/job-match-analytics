import pytest
import os
from unittest.mock import patch, Mock
from retrieve_jobs import GetJobs

@pytest.fixture
def params():
	params = {}
	params["baseUrl"] = "dummy_url"
	params["headers"] = "dummy_headers"
	params["params"] = "dummy_params"

	return params


class TestErrorHandling:
	def test_invalid_fetch_response(self, params):
		with patch("requests.get") as mock_get:
			mock_response = Mock()
			mock_response.json.return_value = {"data": []}
			mock_response.status_code = 200
			mock_get.return_value = mock_response

			jobs = GetJobs()
			assert(len(jobs._fetch(params["baseUrl"], params["headers"],
				params["params"])) == 0)

	def test_no_id(self, params):
		with patch("requests.get") as mock_get:
			mock_response = Mock()
			mock_response.json.return_value = {
				"data": [{"job_title": "Job without ID"}, 
				{"job_id": 132, "job_title": "data analyst"}]
			}

			mock_get.return_value = mock_response

			jobs = GetJobs()
			assert(len(jobs.fetch_jobs(params["baseUrl"], params["headers"],
				[params["params"]])) == 1)

	def test_duplicate_id(self, params):
		with patch("requests.get") as mock_get:
			mock_response = Mock()
			mock_response.json.return_value = {
				"data": [{"job_title": "Data Analyst", "job_id": 132},
				{"job_title": "Data Analyst", "job_id": 132}]
			}

			mock_get.return_value = mock_response

			jobs = GetJobs()
			assert(len(jobs.fetch_jobs(params["baseUrl"], params["headers"],
				[params["params"]])) == 1)