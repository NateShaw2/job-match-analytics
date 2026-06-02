import pytest
import os
from unittest.mock import patch, Mock
from retrieve_jobs import GetJobs

@pytest.fixture
def params():
	params = {}
	params["baseUrl"] = "dummy_url"
	params["headers"] = "dummy_headers"
	params["params"] = {"query": "Data Analyst", "num_pages": "1"}
	return params


class TestErrorHandling:
	def test_invalid_fetch_response(self, params):
		with patch("requests.get") as mock_get:
			mock_response = Mock()
			mock_response.json.return_value = {"error": "invalid request"}
			mock_response.status_code = 200
			mock_get.return_value = mock_response

			jobs = GetJobs()
			assert(len(jobs._fetch(params["baseUrl"], params["headers"],
				params["params"])) == 0)

	def test_no_id(self, params):
		with patch("requests.get") as mock_get:
			mock_response = Mock()
			mock_response.json.return_value = {
				"data": {"jobs":[
					{"job_title": "Job without ID"}, 
					{"job_id": 132, "job_title": "data analyst"}
				]}
			}

			mock_get.return_value = mock_response

			jobs = GetJobs()
			assert(len(jobs.fetch_jobs(params["baseUrl"], params["headers"],
				[params["params"]])) == 1)

	def test_duplicate_id(self, params):
	    with patch("requests.get") as mock_get:
	        mock_response = Mock()
	        mock_response.json.return_value = {
	            "data": {"jobs": [
	                {"job_title": "Data Analyst", "job_id": 132},
	                {"job_title": "Data Analyst", "job_id": 132}
	            ]}
	        }
	        mock_get.return_value = mock_response
	        jobs = GetJobs()
	        result = jobs.fetch_jobs(params["baseUrl"], params["headers"],
	            [params["params"]])
	        assert len(result) == 1
	        assert jobs.jobs[132]["queries"] == [params["params"]["query"]]

	def test_same_id_multiple_queries(self, params):
	    with patch("requests.get") as mock_get:
	        mock_response = Mock()
	        mock_response.json.return_value = {
	            "data": {"jobs": [
	                {"job_title": "Data Analyst", "job_id": 132}
	            ]}
	        }
	        mock_get.return_value = mock_response
	        jobs = GetJobs()
	        result = jobs.fetch_jobs(params["baseUrl"], params["headers"],
	            [
	                {"query": "Data Analyst", "num_pages": "1"},
	                {"query": "Business Analyst", "num_pages": "1"}
	            ])
	        assert len(result) == 1
	        assert jobs.jobs[132]["queries"] == ["Data Analyst", "Business Analyst"]