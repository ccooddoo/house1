import streamlit as st

# Title of the app
st.title("Study Notes Download Center")

# Description
st.write("Welcome to the Study Notes Download Center! Select and download the study materials you need (DBATU University).")

# Define study notes for each year
notes_by_year = {
    "1st Year": {
        "Engineering Mathematics": "engg_math_1.pdf",
        "Physics": "physics_1.pdf",
        "Chemistry": "chemistry_1.pdf",
        "Basic Electrical Engineering": "basic_electrical_1.pdf"
    },
    "2nd Year": {
        "Data Structures": "data_structures.pdf",
        "Database Management Systems": "dbms.pdf",
        "Computer Networks": "computer_networks.pdf",
        "Operating Systems": "operating_systems.pdf"
    },
    "3rd Year": {
        "Software Engineering": "software_engineering.pdf",
        "Machine Learning Basics": "ml_basics.pdf",
        "Cyber Security Introduction": "cyber_security_intro.pdf",
        "Internet of Things Overview": "iot_overview.pdf"
    },
    "4th Year": {
        "Blockchain Notes": "Blockchain.pdf",
        "Big Data Notes": "Bigdata.pdf",
        "Cloud Computing Notes": "cc.pdf",
        "Artificial Intelligence Notes": "Ai.pdf"
    }
}

# Sidebar to select the year
st.sidebar.title("Year Selection")
selected_year = st.sidebar.radio("Select your year", list(notes_by_year.keys()))

# Display notes for the selected year
st.header(f"{selected_year} Study Notes")
notes_for_year = notes_by_year[selected_year]

# Let the user select a note to download
selected_note = st.selectbox("Select Study Material", list(notes_for_year.keys()))

# Provide a download button for the selected note
if st.button("Download"):
    file_path = notes_for_year[selected_note]
    try:
        with open(file_path, "rb") as file:
            st.download_button(
                label="Click here to download",
                data=file,
                file_name=file_path,
                mime="application/pdf"
            )
    except FileNotFoundError:
        st.error(f"The selected file '{file_path}' is not available. Please contact the administrator.")
