import json
import requests

with open('config/config.json', 'r') as file:
    config = json.load(file)

# 生成getToken_URL
getToken_url = config['url_getToken'].format(client_id=config['client_id'],
                                         client_secret=config['client_secret'],
                                         grant_type=config['grant_type'])

def get_access_token(url):
    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    # print(response.json())
    return response.json().get("access_token")


token = get_access_token(getToken_url)
url_XuanYuan= config['url_XuanYuan_70B'] + token


def main():

    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url_XuanYuan, headers=headers, data=payload)
    print(response)

    print(response.text)