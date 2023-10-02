import requests


def check_ipo():
    response = requests.get("http://localhost:8000/ipo")

    if response.status_code == 200:
        return response.json()
    else:
        print(f'Failed: {response.status_code}')