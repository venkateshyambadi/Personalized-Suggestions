import streamlit as st

# Navigation function
def navigate_to_page(page_name):
    st.session_state["current_page"] = page_name
    st.experimental_rerun()
def home_page():
    #add info about the eye disease detection system in the sidebar
    st.sidebar.markdown(
        """
        <h2 style='color: black ; text-align: center; color: red;'>Personalized Medicine Suggestions</h2>
        """,
        unsafe_allow_html=True
    )
    st.sidebar.image('https://static.vecteezy.com/system/resources/previews/024/585/326/non_2x/3d-happy-cartoon-doctor-cartoon-doctor-on-transparent-background-generative-ai-png.png')
    st.sidebar.markdown(
        """
        
        <p style='color: green; text-align: center;'>This web application is designed to recommeds the drugs for various problems using machine learning algorithms.</p>
        """,
        unsafe_allow_html=True
    )
    #type of eye diseases
    st.sidebar.markdown(
        """
        <h3 style='color: maroon; text-align: center;'>Types of Problems</h3>
        """,
        unsafe_allow_html=True
    )
    st.sidebar.markdown(
        """
        <ul>
            <li>Fever</li>
            <li>Cold</li>
            <li>Headache</li>
            <li>Stomach Pain</li>
            <li>Diabetes</li>
            <li>Heart Problems</li>
            <li>Eye Problems</li>
            <li>Ear Problems</li>
            <li>Throat Problems</li>
            <li>Others</li>
        </ul>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
    """
    <style>
    /* Apply background image to the main content area */
    .main {
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-color: rgba(255, 255, 255, 0.8);
        background-blend-mode: fill;
    }
    </style>
    """,
    unsafe_allow_html=True
    )
    st.markdown(
        """
        <div style="text-align: center; padding: 1px; background-color: rgba(78, 78, 6, 0.8); border-radius: 70px;">
            <p style="color: white; font-size: 28px;"><b>Personalized Medicine Suggestions & Remaider System</b></p>
        </div>
        """,
        unsafe_allow_html=True
    )
    #add image
    st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://media.istockphoto.com/id/1210316719/vector/the-team-of-doctors.jpg?s=612x612&w=0&k=20&c=IYaEXKkU11b4GnkkU1uKHrpkgMf_YjziURKkIYHwYsM=" alt="Eye Disease Detection" style="width: 100%; height: 50%;">
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3, col4, col5,col6 = st.columns([1.5, 1, 1, 1, 1,1])
    with col2:
        if st.button("Sign In",type="primary"):
            navigate_to_page("login")
    with col5:
        if st.button("Sign Up",type="primary"):
            navigate_to_page("signup")
