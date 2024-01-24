import requests
import json


def do_request(prompt):
    url = "https://api.baichuan-ai.com/v1/chat/completions"
    api_key = "sk-"

    data = {
        "model": "Baichuan2-Turbo",
        "messages": [
            {
                "role": "user",
                "content": f"\n{prompt}"
            }
        ],
        "stream": False
    }

    json_data = json.dumps(data)

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + api_key
    }

    response = requests.post(url, data=json_data, headers=headers, timeout=60)

    if response.status_code == 200:
        print(response.headers.get("X-BC-Request-Id"))
    else:
        print("请求失败，状态码:", response.status_code)
        print("请求失败，body:", response.text)
        print("请求失败，X-BC-Request-Id:", response.headers.get("X-BC-Request-Id"))


if __name__ == "__main__":
    prompt = '世界第一高峰是'
    do_request(prompt)
