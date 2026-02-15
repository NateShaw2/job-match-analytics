import os
import requests
import json
from dotenv import load_dotenv

class get_jobs:
	def __init__(self, search_terms = [
	    'data analyst',
	    'junior data analyst',
	    'business analyst', 
	    'business intelligence analyst',
	    'junior business analyst',
	    'reporting analyst'
	]):
		self.search_terms = search_terms
		load_dotenv()
		self.app_id = os.getenv("APP_ID")
		self.application_key = os.getenv("APPLICATION_KEY")
		self.baseUrl = os.getenv("BASE_URL")
		self.jobs = []

	def test_fetch(self):
		params = {
			"app_id": self.app_id,
			"app_key": self.application_key,
			"results_per_page": 1,
			"what": self.search_terms[0]
		}

		response = requests.get(self.baseUrl + "/1", params=params)
		data = response.json()

		print(f"Status: {response.status_code}")
		print(f"Results found: {data.get('count', 0)}")

		if data.get("results"):
			print("\nSample job:")
			print(json.dumps(data["results"][0], indent=2))
			return data["results"][0]

		return None

if __name__ == "__main__":
	jobs = get_jobs()
	jobs.test_fetch()