import streamlit as st
from landing import landing_page
from dashboard import dashboard
from student_management import student_management_page

st.set_page_config(
    page_title="PragyanAI",
    layout="wide"
)

# ---------------------------------------------------
# SESSION STATES
# ---------------------------------------------------

if "page" not in st.session_state:
    st.session_state.page = "landing"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# ---------------------------------------------------
# PAGE ROUTING
# ---------------------------------------------------

if st.session_state.page == "landing":

    landing_page()

elif st.session_state.page == "dashboard":

    if st.session_state.logged_in:

        dashboard()

    else:

        st.session_state.page = "landing"

elif st.session_state.page == "students":

    if st.session_state.logged_in:

        student_management_page()

    else:

        st.session_state.page = "landing"
