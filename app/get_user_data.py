import requests


def get_user_data():

    url = "http://127.0.0.1:8000/ask"

  

    try:
        response = requests.get(
            url,
        )

        response.raise_for_status()

        content = response.json()

    except Exception as e:

        print(f"[ERROR] {e}")

        content = {
            "email": "example@gmail.com",
            "role": "user",
            "userID": 123,
            "username": "fuck",
            "language": "en"
        }

    return content