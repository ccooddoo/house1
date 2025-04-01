import streamlit as st import openai import os from PIL import Image import io

Set up OpenAI API key from environment variable

openai.api_key = os.getenv("OPENAI_API_KEY")

if openai.api_key is None: st.error("API key is missing! Set OPENAI_API_KEY in your environment variables.") else: st.title("AI Image Editor") st.write("Upload an image and provide an edit prompt.")

# Upload an image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    # Get user prompt for image edit
    prompt = st.text_area("Enter your image edit request:")

    if st.button("Generate Edited Image") and prompt:
        with st.spinner("Editing image..."):
            try:
                response = openai.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    n=1,
                    size="1024x1024"
                )
                
                edited_image_url = response.data[0].url
                st.image(edited_image_url, caption="Edited Image", use_column_width=True)
                st.write(f"[Download Edited Image]({edited_image_url})")
            except Exception as e:
                st.error(f"Error: {e}")

