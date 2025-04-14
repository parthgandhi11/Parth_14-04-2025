import requests

endpoint='http://localhost:8000/timezones/upload/'

get_response=requests.get(endpoint)
print(get_response.json())