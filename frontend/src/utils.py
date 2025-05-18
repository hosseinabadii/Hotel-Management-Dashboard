import time

import api
import streamlit as st


def rerun() -> None:
    time.sleep(0.5)
    st.rerun()


def check_empty(text: str, message: str) -> bool:
    if text == "":
        st.error(message)
        return True
    return False


def validation_id(id: int) -> None:
    if id <= 0:
        st.error("Customer id must be greater than zero!")
        st.stop()


def get_all_ids(end_point: str) -> list[int] | None:
    response = api.get(end_point)
    if response["status"] == "error":
        st.error(response["message"])
        return
    return [item["id"] for item in response["data"]]


def initialize_customer_session() -> None:
    if "customer" not in st.session_state:
        st.session_state["customer"] = None

    if "find_customer" not in st.session_state:
        st.session_state["find_customer"] = False

    if "update_customer" not in st.session_state:
        st.session_state["update_customer"] = False

    if "delete_customer" not in st.session_state:
        st.session_state["delete_customer"] = False


def initialize_room_session() -> None:
    if "room" not in st.session_state:
        st.session_state["room"] = None

    if "find_room" not in st.session_state:
        st.session_state["find_room"] = False

    if "update_room" not in st.session_state:
        st.session_state["update_room"] = False

    if "delete_room" not in st.session_state:
        st.session_state["delete_room"] = False


def initialize_booking_session() -> None:
    if "booking" not in st.session_state:
        st.session_state["booking"] = None

    if "find_booking" not in st.session_state:
        st.session_state["find_booking"] = False

    if "update_booking" not in st.session_state:
        st.session_state["update_booking"] = False

    if "delete_booking" not in st.session_state:
        st.session_state["delete_booking"] = False
