import streamlit as st
from pages import admin, employee

st.set_page_config(page_title='EMS', page_icon=':office:', layout="wide")

st.sidebar.title('DASHBOARD')
menu_choice = st.sidebar.selectbox('Menu', ('Home',))

if menu_choice == 'Home':
    user_type = st.selectbox('Select', ('Admin login', 'Employee login'))
    if user_type == 'Admin login':
        admin.run_admin()
    else:
        employee.run_employee()
