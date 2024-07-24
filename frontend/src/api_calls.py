from typing import Any

import requests
from loguru import logger

# BASE_URL = "http://127.0.0.1:8000/"
BASE_URL = "http://fastapi-server:8000/"


def get_one(end_point: str) -> dict[str, Any] | str:
    url = BASE_URL + end_point
    try:
        response = requests.get(url)
        if response.status_code == 200:
            logger.success("Fetch data successfully.")
            return response.json()
        return "Failed to fetch data."
    except requests.exceptions.ConnectionError as e:
        logger.error(e)
        return "Something happend!"


def get_all(end_point: str) -> list[dict[str, Any]] | str:
    url = BASE_URL + end_point
    try:
        response = requests.get(url)
        if response.status_code == 200:
            logger.success("Fetch data successfully.")
            return response.json()
        return "Failed to fetch data."
    except requests.exceptions.ConnectionError as e:
        logger.error(e)
        return "Something happend!"


def post(end_point: str, data: dict) -> dict[str, Any] | str:
    url = BASE_URL + end_point
    try:
        response = requests.post(url, json=data)
        if response.status_code == 201:
            logger.success("Create a new entry successfully.")
            return response.json()
        return "Failed to fetch data."
    except requests.exceptions.ConnectionError as e:
        logger.error(e)
        return "Something happend!"


def update(end_point: str, data: dict) -> dict[str, Any] | str:
    url = BASE_URL + end_point
    try:
        response = requests.put(url, json=data)
        if response.status_code == 202:
            logger.success("Delete an entry successfully.")
            return response.json()
        return "Failed to fetch data."
    except requests.exceptions.ConnectionError as e:
        logger.error(e)
        return "Something happend!"


def delete(end_point: str) -> bool | str:
    url = BASE_URL + end_point
    try:
        response = requests.delete(url)
        if response.status_code == 204:
            return True
        return "Failed to fetch data."
    except requests.exceptions.ConnectionError as e:
        logger.error(e)
        return "Something happend!"
