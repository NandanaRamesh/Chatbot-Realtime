import streamlit as st
from streamlit_lottie import st_lottie
import requests
from sign_in_page import sign_in_page
from sign_up_page import sign_up_page

# Function to load a Lottie animation from a URL
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Function for the sidebar buttons and dropdown
def sidebar():
    # Full-width button styling for sidebar
    st.markdown(""" 
        <style> 
        .css-1cpxqw2 { width: 100% !important; }  
        .stButton button { width: 100% !important; }  
        .stSelectbox, .stRadio { width: 100% !important; }  
        .css-1d391kg {
            background-color: #f5f5f5 !important;
            padding: 1em;
        }
        </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        home_button = st.button("Home", key="home_sidebar_1")
        feature_selection = st.selectbox("Features", ["Feature 1", "Feature 2", "Feature 3"], key="features_sidebar_1")

        # Check if signed in
        if st.session_state.get("signed_in", False):
            sign_out_button = st.button("Sign Out", key="sign_out_button_1")
            return home_button, feature_selection, None, None, sign_out_button
        else:
            sign_in_button = st.button("Sign In", key="sign_in_button_1")
            sign_up_button = st.button("Sign Up", key="sign_up_button_1")
            return home_button, feature_selection, sign_in_button, sign_up_button, None




# Title page with typing animation and button
def title_page():
    # Typing animation and blinking cursor CSS
    st.markdown("""
        <style>
        .typewriter h1 {
            overflow: hidden; 
            border-right: .15em solid orange; 
            white-space: nowrap; 
            margin: 0 auto; 
            letter-spacing: .15em;
            animation: 
                typing 2.5s steps(30, end),
                blink-caret .75s step-end infinite;
            font-size: 60px;
            text-align: center;
        }

        @keyframes typing {
            from { width: 0 }
            to { width: 100% }
        }

        @keyframes blink-caret {
            from, to { border-color: transparent }
            50% { border-color: orange; }
        }

        /* Hide button initially */
        #continue-btn {
            display: none;
            text-align: center;
        }

        /* Make button full width */
        #continue-btn button {
            width: 100%;
            font-size: 18px;
            padding: 0.5em 1em;
        }
        </style>

        <div class="typewriter">
            <h1>Personal Assistant</h1>
        </div>
    """, unsafe_allow_html=True)

    # JS to reveal button after animation
    st.markdown("""
        <script>
            setTimeout(() => {
                const btn = window.parent.document.querySelector('[data-testid="stButton"]');
                if (btn) {
                    const wrapper = document.getElementById("continue-btn");
                    if (wrapper) {
                        wrapper.style.display = "block";
                    }
                }
            }, 2700);
        </script>
    """, unsafe_allow_html=True)

    st.markdown("###")

    # Centered button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
                <style>
                    div.stButton > button {
                        width: 100%;
                    }
                </style>
            """, unsafe_allow_html=True)

        if st.button("Continue to app >>"):
            st.session_state.page = "home"

        st.markdown('</div>', unsafe_allow_html=True)

# Function for the home page content
def home_page(home_button, sign_in_button, sign_up_button, sign_out_button):
    # Redirect to Sign In or Sign Up based on button click
    if sign_in_button:
        st.session_state.page = "sign_in"
    elif sign_up_button:
        st.session_state.page = "sign_up"
    # Sign out action
    elif sign_out_button:
        st.session_state.signed_in = False
        st.session_state.page = "home"
        st.rerun()

    
    # Check if the user is signed in or navigate to the appropriate page
    if "page" not in st.session_state:
        st.session_state.page = "home"

    if st.session_state.page == "home":
        # Home page content when signed in
        if "signed_in" in st.session_state and st.session_state.signed_in:
            st.title("Welcome to Your Dashboard")
            st.markdown(
                """
                <style>
                .grid-button {
                    background-color: #373782;
                    color: white;
                    border: none;
                    border-radius: 15px;
                    padding: 3em;
                    font-size: 1.5em;
                    font-weight: bold;
                    width: 100%;
                    height: 100%;
                    text-align: center;
                    transition: 0.3s ease;
                    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
                }

                .grid-button:hover {
                    background-color: #2f2f70;
                    cursor: pointer;
                }

                .grid-container {
                    display: flex;
                    flex-direction: column;
                    gap: 1.5em;
                    margin-top: 2em;
                }

                .grid-row {
                    display: flex;
                    gap: 1.5em;
                }

                .grid-col {
                    flex: 1;
                    display: flex;
                    align-items: stretch;
                }

                .button-wrapper {
                    width: 100%;
                }
                </style>

                <div class="grid-container">
                    <div class="grid-row">
                        <div class="grid-col">
                            <div class="button-wrapper">
                                <button class="grid-button">Memos</button>
                            </div>
                        </div>
                        <div class="grid-col">
                            <div class="button-wrapper">
                                <button class="grid-button">Chat</button>
                            </div>
                        </div>
                    </div>
                    <div class="grid-row">
                        <div class="grid-col">
                            <div class="button-wrapper">
                                <button class="grid-button">Calendar</button>
                            </div>
                        </div>
                        <div class="grid-col">
                            <div class="button-wrapper">
                                <button class="grid-button">Organize</button>
                            </div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            # Show info about the app when not signed in
            st.title("Welcome to Our AI-Powered Personal Assistant!")
            st.write("""
                Our app is a personal assistant powered by AI. 
                It will help you set reminders, keep track of important dates, and more.
                You can use it to manage your calendar, create tasks, and get notifications. 
                Stay organized and on top of your schedule!
            """)
            # Load and show Lottie animation
            lottie_url = "https://assets1.lottiefiles.com/packages/lf20_mjlh3hcy.json"  # Replace with your preferred animation
            lottie_json = load_lottie_url(lottie_url)

            if lottie_json:
                st_lottie(lottie_json, speed=1, height=300, key="ai_lottie")

    elif st.session_state.page == "sign_up":
        # Show the Sign Up page
        sign_up_page()

    elif st.session_state.page == "sign_in":
        # Show the Sign In page
        sign_in_page()

    # Home button action (optional, just for returning to home page)
    if home_button:
        st.session_state.page = "home"


# Main function to handle page navigation
def main():
    if "page" not in st.session_state:
        st.session_state.page = "title"
    if "signed_in" not in st.session_state:
        st.session_state.signed_in = False

    # Page routing logic
    if st.session_state.page == "title":
        title_page()
    else:
        # Call sidebar AFTER state updates
        home_button, feature_selection, sign_in_button, sign_up_button, sign_out_button = sidebar()

        # Handle navigation buttons
        if sign_in_button:
            st.session_state.page = "sign_in"
        elif sign_up_button:
            st.session_state.page = "sign_up"
        elif sign_out_button:
            st.session_state.signed_in = False
            st.session_state.page = "home"
        elif home_button:
            st.session_state.page = "home"

        # Route to the appropriate page
        if st.session_state.page == "home":
            home_page(home_button, sign_in_button, sign_up_button, sign_out_button)
        elif st.session_state.page == "sign_in":
            sign_in_page()
        elif st.session_state.page == "sign_up":
            sign_up_page()


if __name__ == "__main__":
    main()
