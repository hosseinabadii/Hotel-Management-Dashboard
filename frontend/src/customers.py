import pandas as pd
import streamlit as st

from .api_calls import delete, get_one, get_all, post, update
from .utils import check_empty, get_all_ids, initialize_customer_session, rerun


def all_customers():
    st.subheader("All Customers")
    if st.button("Show all customers"):
        response = get_all("customers/")
        if isinstance(response, list):
            if len(response) == 0:
                st.warning("No customers!")
                st.stop()
            data = pd.DataFrame(response)
            data = data.set_index("id")
            data.columns = ["First Name", "Last Name", "Email Address"]
            st.table(data)
        else:
            st.error(response)


def create_customer():
    st.subheader("Create Customer")
    with st.form("create"):
        first_name = st.text_input("First Name: *")
        last_name = st.text_input("Last Name: *")
        email_address = st.text_input("Email Address: *")
        submitted = st.form_submit_button("Create")

    if submitted:
        c1 = check_empty(first_name, "First Name is required!")
        c2 = check_empty(last_name, "Last Name is required!")
        c3 = check_empty(email_address, "Email Address is required!")
        if any((c1, c2, c3)):
            st.stop()
        customer_data = {
            "first_name": first_name,
            "last_name": last_name,
            "email_address": email_address,
        }
        response = post("customer/", customer_data)
        if isinstance(response, dict):
            st.success("A new customer created.")
            st.write(response)
        else:
            st.error(response)


def manage_customer():
    st.subheader("Manage Customer")
    customer_ids = get_all_ids("customers/")
    if customer_ids is None:
        st.stop()
    st.write("Select the customer id:")
    same_id = None
    if st.session_state["customer"]:
        same_id = st.session_state["customer"]["id"]
        index = customer_ids.index(same_id)
        customer_id = st.selectbox(
            "Select Customer id",
            customer_ids,
            index=index,
            label_visibility="collapsed",
        )
    else:
        customer_id = st.selectbox(
            "Select Customer id", customer_ids, index=0, label_visibility="collapsed"
        )

    columns = st.columns([0.2, 0.15, 0.15, 0.5])
    find_customer_button = columns[0].button("Find Customer")
    if find_customer_button and (customer_id is not None) and (same_id != customer_id):
        st.session_state["find_customer"] = True
        find_customer(customer_id)

    customer = st.session_state["customer"]
    if customer:
        st.write(customer)
        update_button = columns[1].button("Update")
        delete_button = columns[2].button("Delete")
        if update_button or st.session_state["update_customer"]:
            st.session_state["update_customer"] = True
            update_customer(customer)
        if delete_button or st.session_state["delete_customer"]:
            st.session_state["delete_customer"] = True
            delete_customer(customer["id"])


def find_customer(customer_id: int):
    if not st.session_state["find_customer"]:
        return
    st.session_state["find_customer"] = False
    response = get_one(f"customer/{customer_id}")
    if isinstance(response, dict):
        st.session_state["customer"] = response
        st.rerun()
    else:
        st.error(response)
        st.session_state["customer"] = None
        rerun()


def update_customer(customer: dict) -> None:
    if not st.session_state["update_customer"]:
        return
    with st.form("update"):
        customer_data = {
            "first_name": st.text_input("First Name:", value=customer["first_name"]),
            "last_name": st.text_input("Last Name:", value=customer["last_name"]),
            "email_address": st.text_input(
                "Email Address:", value=customer["email_address"]
            ),
        }
        submitted = st.form_submit_button("Update")
        if submitted:
            st.session_state["update_customer"] = False
            response = update(f"customer/{customer['id']}", customer_data)
            if isinstance(response, dict):
                st.success("Customer modified.")
                st.session_state["customer"] = response
                rerun()
            else:
                st.error(response)
                rerun()


def delete_customer(customer_id: int) -> None:
    if not st.session_state["delete_customer"]:
        return
    st.warning("Are you sure you want to delete this customer?")
    columns = st.columns([0.1, 0.1, 0.8])
    if columns[0].button("Yes"):
        response = delete(f"customer/{customer_id}")
        if isinstance(response, bool):
            st.success("Customer deleted.")
            st.session_state["customer"] = None
            st.session_state["delete_customer"] = False
            rerun()
        else:
            st.error(response)
            rerun()
    if columns[1].button("No"):
        st.session_state["delete_customer"] = False
        st.write("Deleting Cancelled!")
        rerun()


def customers_view() -> None:
    initialize_customer_session()
    menu_options = [
        "All Customers",
        "Create Customer",
        "Manage Customer",
    ]
    menu_choice = st.sidebar.radio("List of operations:", menu_options)

    if menu_choice == menu_options[0]:
        all_customers()

    if menu_choice == menu_options[1]:
        create_customer()

    if menu_choice == menu_options[2]:
        manage_customer()
