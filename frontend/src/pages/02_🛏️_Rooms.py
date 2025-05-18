import api
import pandas as pd
import streamlit as st
from utils import check_empty, get_all_ids, initialize_room_session, rerun


def all_rooms():
    st.subheader("All Rooms")
    response = api.get("rooms/")
    if response["status"] == "success":
        rooms = response["data"]
        if len(rooms) == 0:
            st.warning("No rooms!")
            st.stop()
        df = pd.DataFrame(rooms)
        df = df.set_index("id")
        df.columns = ["Number", "Size", "Price"]
        st.table(df)
    else:
        st.error(response["message"])


def create_room():
    st.subheader("Create Room")
    with st.form("create"):
        number = st.text_input("Number: *")
        size = st.number_input("Size: *", step=10, min_value=10)
        price = st.number_input(
            "Price in Cent e.g. 1000 = $10.00: *",
            step=10_00,
            min_value=10_00,
        )
        submitted = st.form_submit_button("Create")

    if submitted:
        if check_empty(number, "Number is required!"):
            st.stop()
        room_data = {
            "number": number,
            "size": size,
            "price": price,
        }
        response = api.post("rooms/", room_data)
        if response["status"] == "success":
            room = response["data"]
            st.success("A new room created.")
            st.session_state["room"] = room
            df = pd.DataFrame([room])
            df = df.set_index("id")
            df.columns = ["Number", "Size", "Price"]
            st.table(df)
        else:
            st.error(response["message"])


def manage_room():
    st.subheader("Manage Room")
    room_ids = get_all_ids("rooms/")
    if room_ids is None:
        st.stop()
    st.write("Select the room id:")
    same_id = None
    if st.session_state["room"]:
        same_id = st.session_state["room"]["id"]
        index = room_ids.index(same_id)
        room_id = st.selectbox(
            "Select Room id",
            room_ids,
            index=index,
            label_visibility="collapsed",
        )
    else:
        room_id = st.selectbox("Select Room id", room_ids, label_visibility="collapsed")

    columns = st.columns([0.2, 0.15, 0.15, 0.5])
    find_room_button = columns[0].button("Find Room")
    if find_room_button and (room_id is not None) and (same_id != room_id):
        st.session_state["find_room"] = True
        find_room(room_id)

    room = st.session_state["room"]
    if room:
        df = pd.DataFrame([room])
        df = df.set_index("id")
        df.columns = ["Number", "Size", "Price"]
        st.table(df)
        update_button = columns[1].button("Update")
        delete_button = columns[2].button("Delete")
        if update_button or st.session_state["update_room"]:
            st.session_state["update_room"] = True
            update_room(room)
        if delete_button or st.session_state["delete_room"]:
            st.session_state["delete_room"] = True
            delete_room(room["id"])


def find_room(room_id: int):
    if not st.session_state["find_room"]:
        return
    st.session_state["find_room"] = False
    response = api.get(f"rooms/{room_id}")
    if response["status"] == "success":
        st.session_state["room"] = response["data"]
        st.rerun()
    else:
        st.error(response["message"])
        st.session_state["room"] = None
        rerun()


def update_room(room: dict) -> None:
    if not st.session_state["update_room"]:
        return
    with st.form("update"):
        room_data = {
            "number": st.text_input("Number:", value=room["number"]),
            "size": st.number_input("Size:", value=room["size"], min_value=10, step=10),
            "price": st.number_input(
                "Price in Cent e.g. 1000 = $10.00:",
                value=room["price"],
                min_value=10_00,
                step=10_00,
            ),
        }
        submitted = st.form_submit_button("Update")
        if submitted:
            st.session_state["update_room"] = False
            response = api.update(f"rooms/{room['id']}", room_data)
            if response["status"] == "success":
                st.success("Room modified.")
                st.session_state["room"] = response["data"]
                rerun()
            else:
                st.error(response["message"])
                rerun()


def delete_room(room_id: int) -> None:
    if not st.session_state["delete_room"]:
        return
    st.warning("Are you sure you want to delete this room?")
    columns = st.columns([0.1, 0.1, 0.8])
    if columns[0].button("Yes"):
        response = api.delete(f"rooms/{room_id}")
        if response["status"] == "success":
            st.success("Room deleted.")
            st.session_state["room"] = None
            st.session_state["delete_room"] = False
            rerun()
        else:
            st.error(response["message"])
            rerun()
    if columns[1].button("No"):
        st.session_state["delete_room"] = False
        st.write("Deleting Cancelled!")
        rerun()


def rooms_view() -> None:
    initialize_room_session()
    menu_options = ["All Rooms", "Create Room", "Manage Room"]
    menu_choice = st.sidebar.radio("List of operations:", menu_options)

    if menu_choice == menu_options[0]:
        all_rooms()

    if menu_choice == menu_options[1]:
        create_room()

    if menu_choice == menu_options[2]:
        manage_room()


if __name__ == "__main__":
    rooms_view()
