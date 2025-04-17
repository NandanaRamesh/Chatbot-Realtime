import streamlit as st
from firebase_config import auth

# Sign-up function
def sign_up(email, password):
    # Check for basic input validation
    if not email or not password:
        raise ValueError("Email and password must not be empty.")
        
    user = auth.create_user_with_email_and_password(email, password)

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
