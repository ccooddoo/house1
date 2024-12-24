import streamlit as st

# Title of the app
st.title("Study Notes Download Center")

# Description
st.write("Welcome to the Study Notes Download Center! Select and download the study materials you need.")

# Define study notes for each year and semester
notes_by_year_and_semester = {
    "1st Year": {
        "Semester 1": {
            "Engineering Mathematics I": "engg_math_1.pdf",
            "Physics": "physics_1.pdf",
            "Chemistry": "chemistry_1.pdf",
            "Basic Electrical Engineering": "basic_electrical_1.pdf"
        },
        "Semester 2": {
            "Engineering Mathematics II": "engg_math_2.pdf",
            "Environmental Science": "env_sci.pdf",
            "Basic Civil Engineering": "basic_civil.pdf",
            "Programming in C": "programming_in_c.pdf"
        }
    },
    "2nd Year": {
        "Semester 3": {
            "Data Structures": "data_structures.pdf",
            "Database Management Systems": "dbms.pdf",
            "Computer Networks": "computer_networks.pdf",
            "Digital Electronics": "digital_electronics.pdf"
        },
        "Semester 4": {
            "Operating Systems": "operating_systems.pdf",
            "Theory of Computation": "toc.pdf",
            "Software Engineering": "software_engineering.pdf",
            "Microprocessors": "microprocessors.pdf"
        }
    },
    "3rd Year": {
        "Semester 5": {
            "Machine Learning Basics": "ml_basics.pdf",
            "Cyber Security Introduction": "cyber_security_intro.pdf",
            "Internet of Things Overview": "iot_overview.pdf",
            "Advanced Algorithms": "advanced_algorithms.pdf"
        },
        "Semester 6": {
            "Machine Learning Advanced": "ml_advanced.pdf",
            "Software Testing": "software_testing.pdf",
            "Cyber Security Advanced": "cyber_security_advanced.pdf",
            "IoT Applications": "iot_applications.pdf"
        }
    },
    "4th Year": {
        "Semester 7": {
            "Artificial Intelligence": "Ai.pdf",
            "Cloud Computing": "cc.pdf",
            "Big Data": "Bigdata.pdf",
            "Blockchain": "Blockchain.pdf"
        },
        "Semester 8": {
            "Research Project": "research_project.pdf",
            "Distributed Systems": "distributed_systems.pdf",
            "Ethical Hacking": "ethical_hacking.pdf",
            "Deep Learning": "deep_learning.pdf"
        }
    }
}

# Sidebar to select the year
st.sidebar.title("Year Selection")
selected_year = st.sidebar.radio("Select your year", list(notes_by_year_and_semester.keys()))

# Sidebar to select the semester
selected_semester = st.sidebar.radio(
    "Select your semester", list(notes_by_year_and_semester[selected_year].keys())
)

# Display notes for the selected semester
st.header(f"{selected_year} - {selected_semester} Study Notes")
notes_for_semester = notes_by_year_and_semester[selected_year][selected_semester]

# Let the user select a note to download
selected_note = st.selectbox("Select Study Material", list(notes_for_semester.keys()))

# Provide a download button for the selected note
if st.button("Download"):
    file_path = notes_for_semester[selected_note]
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
