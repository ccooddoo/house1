import streamlit as st

# Title of the app
st.title("Study Notes Download Center")

# Description
st.write("Welcome to the Study Notes Download Center! Select and download the study materials you need.")

# Pre-defined study notes (you can add more files or categories)
study_notes = {
    "Mathematics Notes": "mathematics_notes.pdf",
    "Physics Notes": "physics_notes.pdf",
    "Chemistry Notes": "chemistry_notes.pdf",
    "Biology Notes": "biology_notes.pdf"
}

# Let user select a note to download
selected_note = st.selectbox("Select Study Material", list(study_notes.keys()))

# Provide a download button for the selected note
if st.button("Download"):
    file_path = study_notes[selected_note]
    try:
        with open(file_path, "rb") as file:
            st.download_button(
                label="Click here to download",
                data=file,
                file_name=file_path,
                mime="application/pdf"
            )
    except FileNotFoundError:
        st.error("The selected file is not available. Please contact the administrator.")
