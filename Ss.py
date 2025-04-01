import streamlit as st
import openai
from PIL import Image

# Load API key from Streamlit Secrets
if "OPENAI_API_KEY" in st.secrets:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
else:
    st.error("API key is missing! Add it to Streamlit Secrets.")

st.title("AI Image Editor")
st.write("Upload an image and provide an edit prompt.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    prompt = st.text_area("Enter your image edit request:")

    if st.button("Generate Edited Image") and prompt:
        with st.spinner("Editing image..."):
            try:
                response = openai.Image.create(
                    prompt=prompt,
                    n=1,
                    size="1024x1024"
                )

                # Get the URL of the generated image
                edited_image_url = response['data'][0]['url']
                st.image(edited_image_url, caption="Edited Image", use_column_width=True)
                st.write(f"[Download Edited Image]({edited_image_url})")

            except openai.error.AuthenticationError:
                st.error("Invalid API Key! Check your OpenAI API Key in Streamlit Secrets.")
            except Exception as e:
                st.error(f"Error: {e}")
