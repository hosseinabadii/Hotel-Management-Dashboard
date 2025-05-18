import os
from typing import Any

import httpx
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
TIMEOUT = 30.0


def _make_request(method: str, endpoint: str, data: dict | None = None, params: dict | None = None) -> dict[str, Any]:
    """Generic request handler"""
    url = f"{BASE_URL}/{endpoint}"
    response_data = None

    try:
        with httpx.Client(timeout=TIMEOUT) as client:
            response = client.request(method, url, json=data, params=params)

            if 200 <= response.status_code < 300:
                response_data = response.json() if response.content else None
                return {
                    "status": "success",
                    "message": "Request completed successfully",
                    "data": response_data,
                    "status_code": response.status_code,
                }

            error_message = f"API request failed with status {response.status_code}"
            if response.content:
                try:
                    error_data: dict = response.json()
                    error_message = error_data.get("detail", error_data.get("message", error_message))
                except ValueError:
                    error_message = response.text or error_message

            return {"status": "error", "message": error_message, "data": None, "status_code": response.status_code}

    except httpx.RequestError as e:
        error_msg = f"Network error: {str(e)}"
        logger.error(error_msg)
        return {"status": "error", "message": error_msg, "data": None, "status_code": None}
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(error_msg)
        return {"status": "error", "message": error_msg, "data": None, "status_code": None}


def get(endpoint: str) -> dict[str, Any]:
    """Get one or more items"""
    return _make_request("GET", endpoint)


def post(endpoint: str, data: dict) -> dict[str, Any]:
    """Create a new item"""
    return _make_request("POST", endpoint, data=data)


def update(endpoint: str, data: dict) -> dict[str, Any]:
    """Update an existing item"""
    return _make_request("PUT", endpoint, data=data)


def delete(endpoint: str) -> dict[str, Any]:
    """Delete an item"""
    return _make_request("DELETE", endpoint)
