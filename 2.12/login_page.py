import streamlit as st
from database import authenticate_user
def navigate_to_page(page_name):
    st.session_state["current_page"] = page_name
    st.experimental_rerun()

def login_page():
    # Center the login form using Streamlit form layout
    st.markdown(
    """
    <style>
    /* Apply background image to the main content area */
    .main {
        background-image: url("https://img.freepik.com/premium-photo/scientific-molecule-background-with-flow-waves-medicine-science-technology-chemistry-wallpaper-o_230610-906.jpg");  
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }
    </style>
    """,
    unsafe_allow_html=True
    )
    with st.form(key="login_form"):
        # Title
        col1,col2=st.columns([10,1])
        col1.title("Sign In Here !!!")
        if col2.form_submit_button("🏚️"):
            navigate_to_page("home")

        # Email and Password inputs
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        # Submit button inside the form
        col1,col2,col3=st.columns([1,2,1])
        with col1:
            if st.form_submit_button("Login 🔐"):
                if authenticate_user(email, password):
                    st.success(f"Login successful.")
                    st.session_state["logged_in"] = True
                    st.session_state["current_user"] = email

                    navigate_to_page("user_home")
                else:
                    st.error("Invalid email or password.")
        with col3:
            if st.form_submit_button("Create account👤"):
                navigate_to_page("signup")