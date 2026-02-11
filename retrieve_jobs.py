import os
import requests
from dotenv import load_dotenv

class get_jobs:
	def __init__(self, search_terms=['data analyst', 'junior data analyst', 'data analyst entry level', 'business analyst', 'business intelligence developer']):
		self.search_terms = search_terms
		load_dotenv()
		self.app_id = os.getenv("APP_ID")
		self.application_key = os.getenv("APP_ID")

if __name__ == "__main__":
	load_dotenv()
	app_id = os.getenv("APP_ID")
	print(app_id)