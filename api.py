import requests
from typing import Dict, Optional, Any, List
MAX_RESULTS_PER_REQUEST = 500
MAX_RETRIES = 20
def _clean_parameters(parameters: Dict[str, Any]) -> Dict[str, str]:
	""" Removes entries which have no value."""

	return {k: str(v) for k, v in parameters.items() if v}

def get(url: str, parameters: Dict):
	parameters = _clean_parameters(parameters)

	for attempt_number in range(MAX_RETRIES):
		response = query(url, parameters)
		if response:
			break
	else:
		raise Exception("Unable to connect to pushshift.io. Max retries exceeded.")
	return response

def query(url:str, parameters:Dict = None)->List:
	if parameters is None:
		parameters = dict()
	try:
		response = requests.get(url, params = parameters)
		if response.status_code == 200:
			response = response.json()['data']
	except requests.ConnectionError:
		response = None
	return response


