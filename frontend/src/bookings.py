from datetime import date, datetime, timedelta

import pandas as pd
import streamlit as st

from .api_calls import delete, get_all, get_one, post, update
from .utils import get_all_ids, initialize_booking_session, rerun


def all_bookings():
    st.subheader("All Bookings")
    if st.button("Show all Bookings"):
        response = get_all("bookings/")
        if isinstance(response, list):
            if len(response) == 0:
                st.warning("No bookings!")
                st.stop()
            data = pd.DataFrame(response)
            data = data.set_index("id")
            data.columns = ["Room ID", "Customer ID", "Price", "From Date", "To Date"]
            st.table(data)
        else:
            st.error(response)


def create_booking():
    st.subheader("Create Booking")
    today = date.today()
    tomorrow = date.today() + timedelta(days=1)
    room_ids = get_all_ids("rooms/")
    if room_ids is None:
        st.stop()
    customer_ids = get_all_ids("customers/")
    if customer_ids is None:
        st.stop()
    with st.form("create"):
        room_id = st.selectbox("Select Room ID:", room_ids)
        customer_id = st.selectbox("Select Customer ID:", customer_ids)
        from_date = st.date_input("From Date *", min_value=today, value=today)
        to_date = st.date_input("To Date: *", min_value=tomorrow, value=tomorrow)

        submitted = st.form_submit_button("Create")

    if submitted:
        booking_data = {
            "room_id": room_id,
            "customer_id": customer_id,
            "from_date": from_date.strftime("%Y-%m-%d"),  # type: ignore
            "to_date": to_date.strftime("%Y-%m-%d"),  # type: ignore
        }
        response = post("booking/", booking_data)
        if isinstance(response, dict):
            st.success("A new booking created.")
            st.write(response)
        else:
            st.error(response)


def manage_booking():
    st.subheader("Manage Booking")
    booking_ids = get_all_ids("bookings/")
    if booking_ids is None:
        st.stop()
    st.write("Select the booking id:")
    same_id = None
    if st.session_state["booking"]:
        same_id = st.session_state["booking"]["id"]
        index = booking_ids.index(same_id)
        booking_id = st.selectbox(
            "Select Booking id",
            booking_ids,
            index=index,
            label_visibility="collapsed",
        )
    else:
        booking_id = st.selectbox(
            "Select Booking id", booking_ids, label_visibility="collapsed"
        )

    columns = st.columns([0.2, 0.15, 0.15, 0.5])
    find_booking_button = columns[0].button("Find Booking")
    if find_booking_button and (booking_id is not None) and (same_id != booking_id):
        st.session_state["find_booking"] = True
        find_booking(booking_id)

    booking = st.session_state["booking"]
    if booking:
        st.write(booking)
        update_button = columns[1].button("Update")
        delete_button = columns[2].button("Delete")
        if update_button or st.session_state["update_booking"]:
            st.session_state["update_booking"] = True
            update_booking(booking)
        if delete_button or st.session_state["delete_booking"]:
            st.session_state["delete_booking"] = True
            delete_booking(booking["id"])


def find_booking(booking_id: int):
    if not st.session_state["find_booking"]:
        return
    st.session_state["find_booking"] = False
    response = get_one(f"booking/{booking_id}")
    if isinstance(response, dict):
        st.session_state["booking"] = response
        st.rerun()
    else:
        st.error(response)
        st.session_state["booking"] = None
        rerun()


def update_booking(booking: dict) -> None:
    if not st.session_state["update_booking"]:
        return

    today = date.today()
    tomorrow = date.today() + timedelta(days=1)
    room_ids = get_all_ids("rooms/")
    if room_ids is None:
        st.stop()
    customer_ids = get_all_ids("customers/")
    if customer_ids is None:
        st.stop()
    current_room_index = room_ids.index(booking["room_id"])
    current_customer_index = customer_ids.index(booking["customer_id"])
    with st.form("update"):
        booking_data = {
            "room_id": st.selectbox(
                "Select Room ID:", room_ids, index=current_room_index
            ),
            "customer_id": st.selectbox(
                "Select Customer ID:", customer_ids, index=current_customer_index
            ),
            "from_date": st.date_input(
                "From Date *",
                min_value=today,
                value=datetime.strptime(booking["from_date"], "%Y-%m-%d"),
            ).strftime("%Y-%m-%d"),  # type: ignore
            "to_date": st.date_input(
                "To Date *",
                min_value=tomorrow,
                value=datetime.strptime(booking["to_date"], "%Y-%m-%d"),
            ).strftime("%Y-%m-%d"),  # type: ignore
        }
        submitted = st.form_submit_button("Update")
        if submitted:
            st.session_state["update_booking"] = False
            response = update(f"booking/{booking['id']}", booking_data)
            if isinstance(response, dict):
                st.success("Booking modified.")
                st.session_state["booking"] = response
                rerun()
            else:
                st.error(response)
                rerun()


def delete_booking(booking_id: int) -> None:
    if not st.session_state["delete_booking"]:
        return
    st.warning("Are you sure you want to delete this booking?")
    columns = st.columns([0.1, 0.1, 0.8])
    if columns[0].button("Yes"):
        response = delete(f"booking/{booking_id}")
        if isinstance(response, bool):
            st.success("Booking deleted.")
            st.session_state["booking"] = None
            st.session_state["delete_booking"] = False
            rerun()
        else:
            st.error(response)
            rerun()
    if columns[1].button("No"):
        st.session_state["delete_booking"] = False
        st.write("Deleting Cancelled!")
        rerun()


def bookings_view() -> None:
    initialize_booking_session()
    menu_options = [
        "All Bookings",
        "Create Booking",
        "Manage Booking",
    ]
    menu_choice = st.sidebar.radio("List of operations:", menu_options)

    if menu_choice == menu_options[0]:
        all_bookings()

    if menu_choice == menu_options[1]:
        create_booking()

    if menu_choice == menu_options[2]:
        manage_booking()
