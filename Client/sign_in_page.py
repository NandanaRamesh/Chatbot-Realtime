import streamlit as st
from firebase_config import auth
from requests.exceptions import HTTPError
import json

# Sign-in function
def sign_in(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        st.success("Logged in!")
        return user
    except HTTPError as http_err:
        message = "Login failed."
        try:
            error_payload = json.loads(http_err.args[1])
            firebase_message = error_payload.get("error", {}).get("message", "")
            if firebase_message == "INVALID_PASSWORD":
                message = "Incorrect password. Please try again."
            elif firebase_message == "EMAIL_NOT_FOUND":
                message = "No account found with this email."
            elif firebase_message == "USER_DISABLED":
                message = "This account has been disabled."
            elif firebase_message:
                message = firebase_message
        except (IndexError, json.JSONDecodeError, AttributeError):
            message = str(http_err)
        st.error(message)
    except Exception as e:
        st.error(f"Login failed: {e}")


def sign_in_page():
    st.title("Sign In Page")

    with st.form("signin_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Log In")

        if submitted:
            user = sign_in(email, password)
            if user:
                st.session_state.signed_in = True
                st.session_state.page = "home"  # optionally route back to home
                st.rerun()  # 🔁 force app to re-render with updated session state
