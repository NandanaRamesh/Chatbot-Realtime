import streamlit as st
from firebase_config import auth
from requests.exceptions import HTTPError
import json

# Sign-up function
def sign_up(email, password):
    # Check for basic input validation
    if not email or not password:
        raise ValueError("Email and password must not be empty.")

    try:
        user = auth.create_user_with_email_and_password(email, password)
    except HTTPError as http_err:
        message = "Registration failed."
        try:
            error_payload = json.loads(http_err.args[1])
            firebase_message = error_payload.get("error", {}).get("message", "")
            if "WEAK_PASSWORD" in firebase_message:
                message = "Password must be at least 6 characters long."
            elif "EMAIL_EXISTS" in firebase_message:
                message = "An account with this email already exists. Try signing in instead."
            elif "INVALID_EMAIL" in firebase_message:
                message = "Please provide a valid email address."
            else:
                message = firebase_message or message
        except (IndexError, json.JSONDecodeError, AttributeError):
            message = str(http_err)
        st.error(message)
        return None
    except Exception as exc:
        st.error(f"Registration failed: {exc}")
        return None

    # Check if the user is created (you can add more logic if needed here)
    if user:
        st.success("✅ User created successfully!")
        return user 


# Sign-up page logic
def sign_up_page():
    st.title("Sign Up Page")

    with st.form("signup_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Register")

        if submitted:
            user = sign_up(email, password)
            if user:
                st.success("✅ Account created successfully! Please verify your email and sign in.")
