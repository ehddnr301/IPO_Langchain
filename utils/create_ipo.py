import requests


def create_ipo(title, result):
    data = {
        "title": title,
        "query": result["query"],
        "result": result["result"],
        "source_documents": [res["page_content"] for res in result["source_documents"]],
    }
    print(data)
    headers = {'Content-Type': 'application/json', 'accept': 'application/json'}

    response = requests.post("http://localhost:8000", headers=headers, json=data)

    if response.status_code == 200:
        print(f'Success: {response.json()}')
    else:
        print(f'Failed: {response.status_code}')