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
        self.jobs: dict = {}

    def _fetch(self, baseUrl: str, headers: dict, params: dict, verbose: bool = False) -> list:
        if verbose:
            print(f"baseUrl: {baseUrl}\nParams: {params}")
        response = requests.get(baseUrl, headers=headers, params=params)
        data = response.json()
        try:
            data = data["data"]["jobs"]
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

    def fetch_jobs(self, baseUrl: str, headers: dict, paramList: list[dict], verbose: bool = False) -> dict:
        for params in paramList:
            results = self._fetch(baseUrl, headers, params, verbose)
            query = params["query"]
            for result in results:
                try:
                    result_id = result["job_id"]
                except KeyError:
                    logging.error(f"No job id found for result: {json.dumps(result, indent=2)}")
                else:
                    if result_id not in self.jobs:
                        self.jobs[result_id] = result
                        self.jobs[result_id]["queries"] = [query]
                    else:
                        if query not in self.jobs[result_id]["queries"]:
                            self.jobs[result_id]["queries"].append(query)
        return self.jobs