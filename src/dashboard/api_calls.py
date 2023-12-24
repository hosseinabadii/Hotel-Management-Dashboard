import json

import requests

BASE_URL = "http://127.0.0.1:8000/"


def get(end_point: str):
    url = BASE_URL + end_point
    response = requests.get(url)
    if response.status_code == 200:
        return json.loads(response.text)
    return "Failed to fetch data."


def post(end_point: str, data: dict):
    url = BASE_URL + end_point
    response = requests.post(url, json=data)
    if response.status_code == 201:
        return json.loads(response.text)
    return "Failed to fetch data."


def update(end_point: str, data: dict):
    url = BASE_URL + end_point
    response = requests.put(url, json=data)
    if response.status_code == 202:
        return json.loads(response.text)
    return "Failed to fetch data."


def delete(end_point: str):
    url = BASE_URL + end_point
    response = requests.delete(url)
    if response.status_code == 204:
        return True
    return "Failed to fetch data."
