import os
from typing import Any

import requests
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

BASE_URL = os.getenv("BASE_URL")


def get_one(end_point: str) -> dict[str, Any] | str:
    url = f"{BASE_URL}/{end_point}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            logger.success("Fetch data successfully.")
            return response.json()
        logger.error("Failed to fetch data.")
        return "Failed to fetch data."
    except requests.exceptions.ConnectionError as e:
        logger.error(e)
        return "Something happend!"


def get_all(end_point: str) -> list[dict[str, Any]] | str:
    url = f"{BASE_URL}/{end_point}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            logger.success("Fetch data successfully.")
            return response.json()
        logger.error("Failed to fetch data.")
        return "Failed to fetch data."
    except requests.exceptions.ConnectionError as e:
        logger.error(e)
        return "Something happend!"


def post(end_point: str, data: dict) -> dict[str, Any] | str:
    url = f"{BASE_URL}/{end_point}"
    try:
        response = requests.post(url, json=data)
        if response.status_code == 201:
            logger.success("Create a new entry successfully.")
            return response.json()
        logger.error("Failed to fetch data.")
        return "Failed to fetch data."
    except requests.exceptions.ConnectionError as e:
        logger.error(e)
        return "Something happend!"


def update(end_point: str, data: dict) -> dict[str, Any] | str:
    url = f"{BASE_URL}/{end_point}"
    try:
        response = requests.put(url, json=data)
        if response.status_code == 202:
            logger.success("Update an entry successfully.")
            return response.json()
        logger.error("Failed to fetch data.")
        return "Failed to fetch data."
    except requests.exceptions.ConnectionError as e:
        logger.error(e)
        return "Something happend!"


def delete(end_point: str) -> bool | str:
    url = f"{BASE_URL}/{end_point}"
    try:
        response = requests.delete(url)
        if response.status_code == 204:
            logger.success("Delete an entry successfully.")
            return True
        logger.error("Failed to fetch data.")
        return "Failed to fetch data."
    except requests.exceptions.ConnectionError as e:
        logger.error(e)
        return "Something happend!"
