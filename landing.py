import streamlit as st
from auth import (
    login_user,
    register_user,
    reset_password
)


def landing_page():

    # ---------------------------------------------------
    # PAGE STYLE
    # ---------------------------------------------------

    st.markdown("""
    <style>

    .stApp {
        background: linear-gradient(135deg, #8ea6d1, #d4a5c9);
    }

    header {
        visibility: hidden;
    }

    .main-box {
        background: rgba(255,255,255,0.15);
        padding: 40px;
        border-radius: 20px;
        backdrop-filter: blur(10px);
    }

    .title {
        text-align:center;
        font-size:40px;
        font-weight:bold;
        color:#0f172a;
        margin-bottom:20px;
    }

    .stTextInput input {
        background: transparent !important;
        border: none !important;
        border-bottom: 2px solid #1e293b !important;
        border-radius: 0 !important;
        color: #1e293b !important;
    }

    .stButton button {
        width:100%;
        background:#0f172a;
        color:white;
        padding:12px;
        border:none;
        border-radius:10px;
        font-weight:bold;
    }

    .stRadio > div {
        justify-content:center;
    }

    </style>
    """, unsafe_allow_html=True)

    # ---------------------------------------------------
    # CENTER BOX
    # ---------------------------------------------------

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        st.markdown("<div class='main-box'>", unsafe_allow_html=True)

        st.markdown(
            "<div class='title'>PragyanAI Login System</div>",
            unsafe_allow_html=True
        )

        option = st.radio(
            "",
            [
                "Login",
                "Register",
                "Forgot Password"
            ],
            horizontal=True
        )

        # ===================================================
        # LOGIN
        # ===================================================

        if option == "Login":

            username = st.text_input("Username")

            password = st.text_input(
                "Password",
                type="password"
            )

            if st.button("LOGIN"):

                if login_user(username, password):

                    st.session_state.logged_in = True
                    st.session_state.page = "dashboard"
                    st.session_state.user = username

                    st.rerun()

                else:

                    st.error("Invalid Credentials")

        # ===================================================
        # REGISTER
        # ===================================================

        elif option == "Register":

            username = st.text_input("Create Username")

            password = st.text_input(
                "Create Password",
                type="password"
            )

            if st.button("REGISTER"):

                if register_user(username, password):

                    st.success("Registered Successfully ✅")

                else:

                    st.error("User already exists")

        # ===================================================
        # FORGOT PASSWORD
        # ===================================================

        elif option == "Forgot Password":

            username = st.text_input("Enter Username")

            new_password = st.text_input(
                "Enter New Password",
                type="password"
            )

            confirm_password = st.text_input(
                "Confirm New Password",
                type="password"
            )

            if st.button("RESET PASSWORD"):

                if new_password != confirm_password:

                    st.error("Passwords do not match")

                else:

                    success = reset_password(
                        username,
                        new_password
                    )

                    if success:

                        st.success(
                            "Password Reset Successfully ✅"
                        )

                    else:

                        st.error("Username not found")

        st.markdown("</div>", unsafe_allow_html=True)
