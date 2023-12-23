import streamlit as st

from dashboard.bookings import bookings_view
from dashboard.customers import customers_view
from dashboard.rooms import rooms_view
from run_server import start_server

start_server()

st.title("Hotel Management System")

st.sidebar.title("Dashboard")
menu_options = ["Customers", "Rooms", "Bookings"]
menu_choice = st.sidebar.radio("Menu", menu_options)
st.sidebar.subheader("Operations")

if menu_choice == "Customers":
    customers_view()

elif menu_choice == "Rooms":
    rooms_view()

elif menu_choice == "Bookings":
    bookings_view()
