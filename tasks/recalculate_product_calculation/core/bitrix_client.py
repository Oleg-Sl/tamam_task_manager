import os
import requests


class BitrixClient:
    def __init__(self):
        self.webhook = os.getenv('WEBHOOK')

    def call(self, method: str, body: dict):
        url = f'{self.webhook}{method}'
        try:
            response = requests.post(url, json=body)
            if response.ok:
                result = response.json()
                return result
        except Exception as err:
            print(err)
