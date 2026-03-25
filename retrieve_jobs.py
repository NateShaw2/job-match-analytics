import os
import requests
import json
import logging
from dotenv import load_dotenv

logging.basicConfig(
	filename='jobs.log',
	level=logging.WARNING,
	format='%(asctime)s - %(levelname)s - %(message)s'
)

class GetJobs:
	def __init__(self):
		self.jobs = {}

	def _fetch(self, baseUrl, headers, params, verbose=False):
		if verbose:
			print(f"baseUrl: {baseUrl}\nParams: {params}")

		response = requests.get(baseUrl, headers=headers, params=params)
		data = response.json()
		try: 
			data = data['data']
		except KeyError:
			logging.error(f"Could not find job applications for {data}")
			return []

		if verbose:
			print(f"Status: {response.status_code}")
			print(f"Results found: {len(data)}")

		if data:
			if verbose:
				print("\nSample job:")
				print(json.dumps(data[0], indent=2))
			return data

		logging.warning(f"No results found for params: {params}")
		return []

	def fetch_jobs(self, baseUrl, headers, paramList, verbose=False):
		for params in paramList:
			results = self._fetch(baseUrl, headers, params, verbose)
			for result in results:
				try:
					resultID = result["job_id"]
				except KeyError:
					logging.error(f"No job id found for result: {json.dumps(result, indent=2)}")
				else:
					if resultID not in self.jobs:
						self.jobs[resultID] =  result

		return self.jobs


if __name__ == "__main__":
	jobs = GetJobs()

	load_dotenv()
	host = os.getenv("RAPIDAPI_HOST")
	key = os.getenv("RAPIDAPI_KEY")
	baseUrl = os.getenv("BASE_URL")

	headers = {
		"x-rapidapi-key": key,
		"x-rapidapi-host": host,
		"Content-Type": "application/json"
	}

	paramList = [{
		"query": "Data Analyst",
		"num_pages": "1",
		"country": "us",
		"date_posted": "month"
	}]

	print(jobs.fetch_jobs(baseUrl, headers, paramList, verbose=True))