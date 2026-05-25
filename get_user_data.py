import requests

url = "http://127.0.0.1:8000/ask"

params = {
    "query": "How do I register?"
}

response = requests.get(
    url,
    params=params
)

print(response.status_code)
print(response.json())