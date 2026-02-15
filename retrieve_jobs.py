import os
import requests
import json
from dotenv import load_dotenv

class GetJobs:
	def __init__(self, search_terms = [
	    "data analyst remote",
	    "junior data analyst remote",
	    "business analyst remote", 
	    "business intelligence analyst remote",
	    "junior business analyst remote",
	    "reporting analyst remote"
	]):
		self.search_terms = search_terms
		load_dotenv()
		self.app_id = os.getenv("APP_ID")
		self.application_key = os.getenv("APPLICATION_KEY")
		self.baseUrl = os.getenv("BASE_URL")
		self.jobs = {}

	def _fetch(self, search_terms, page_number=2, results_per_page=50, verbose=False):
		params = {
			"app_id": self.app_id,
			"app_key": self.application_key,
			"results_per_page": results_per_page,
			"what": search_terms
		}

		response = requests.get(self.baseUrl + "/" + str(page_number), params=params)
		data = response.json()

		if verbose:
			print(f"Status: {response.status_code}")
			print(f"Results found: {data.get('count', 0)}")

		if data.get("results"):
			if verbose:
				print("\nSample job:")
				print(json.dumps(data["results"][0], indent=2))
			return data["results"]

		return []

	def fetch_jobs(self, pages=2, results_per_page=50, verbose=True):
		for search_term in self.search_terms:
			for page in range(1, pages + 1):
				results = self._fetch(search_term, page, results_per_page=results_per_page)
				for result in results:
					resultID = result["id"]
					if resultID not in self.jobs:
						self.jobs[resultID] =  result

		if verbose:
			print(json.dumps(self.jobs, indent=2))
		return self.jobs


if __name__ == "__main__":
	jobs = GetJobs()
	jobs.fetch_jobs(verbose=True)