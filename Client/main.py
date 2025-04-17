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
        /* Make sidebar button full width */
        .css-1cpxqw2 { width: 100% !important; }  /* Full width button styling */ 
        .stButton button { width: 100% !important; }  /* Full width button */
        
        /* Full width for the selectbox and radio buttons */
        .stSelectbox, .stRadio { width: 100% !important; }  /* Full width dropdown */
        
        /* Customizing the sidebar background */
        .css-1d391kg {
            background-color: #f5f5f5 !important;  /* Customize background color */
            padding: 1em;
        }
        </style>
    """, unsafe_allow_html=True)

    # Sidebar contents
    with st.sidebar:
        # Home button (just a placeholder for navigation)
        home_button = st.button("Home", key="home_sidebar_1")
        
        # Features dropdown (non-typable)
        feature_selection = st.selectbox("Features", ["Feature 1", "Feature 2", "Feature 3"], key="features_sidebar_1")
        
        # Profile buttons for Sign In and Sign Up
        sign_in_button = st.button("Sign In", key="sign_in_button_1")
        sign_up_button = st.button("Sign Up", key="sign_up_button_1")

    return home_button, feature_selection, sign_in_button, sign_up_button


home_button, feature_selection, sign_in_button, sign_up_button = sidebar()

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
def home_page():

   

    # Redirect to Sign In or Sign Up based on button click
    if sign_in_button:
        st.session_state.page = "sign_in"
    elif sign_up_button:
        st.session_state.page = "sign_up"
    
    # Check if the user is signed in or navigate to the appropriate page
    if "page" not in st.session_state:
        st.session_state.page = "home"

    if st.session_state.page == "home":
        # Home page content when signed in
        if "signed_in" in st.session_state and st.session_state.signed_in:
            st.title("Welcome to Your Dashboard")
            card_titles = ["Card 1", "Card 2", "Card 3", "Card 4"]
            cols = st.columns(4)
            for i, col in enumerate(cols):
                with col:
                    st.markdown(f"""
                        <div style='padding: 1em; border-radius: 10px; background-color: #f0f2f6; text-align: center;'>
                            <h4>{card_titles[i]}</h4>
                        </div>
                    """, unsafe_allow_html=True)
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

    # Page routing logic
    if st.session_state.page == "title":
        title_page()
    elif st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "sign_in":
        sign_in_page()
    elif st.session_state.page == "sign_up":
        sign_up_page()

    # Redirect to Sign In or Sign Up based on button click
    if sign_in_button:
        st.session_state.page = "sign_in"
    elif sign_up_button:
        st.session_state.page = "sign_up"

    # Handle home button action
    if home_button:
        st.session_state.page = "home"


if __name__ == "__main__":
    main()
