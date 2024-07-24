import streamlit as st
from src.bookings import bookings_view
from src.customers import customers_view
from src.rooms import rooms_view

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
