import streamlit as st
from firebase_config import auth

# Sign-in function
def sign_in(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        st.success("Logged in!")
        return user
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
