import requests

endpoint='http://localhost:8000/get_report/f171f9bd-bb14-4b5e-ab8f-b74e16a6e57b'

get_response=requests.get(endpoint)
print(get_response.json())