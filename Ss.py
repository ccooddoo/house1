import streamlit as st
import openai
from PIL import Image
import io

# Set up OpenAI API key
openai.api_key = "your_openai_api_key"

st.title("AI Image Editor")
st.write("Upload an image and provide an edit prompt.")

# Upload an image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    # Get user prompt
    prompt = st.text_area("Enter your image edit request:")

    if st.button("Generate Edited Image") and prompt:
        with st.spinner("Editing image..."):
            try:
                # OpenAI now uses assistants for image generation/editing
                response = openai.images.generate(
                    model="dall-e-3",  # Use the latest model
                    prompt=prompt,
                    n=1,
                    size="1024x1024"
                )
                
                # Get edited image URL
                edited_image_url = response.data[0].url
                st.image(edited_image_url, caption="Edited Image", use_column_width=True)
                st.write(f"[Download Edited Image]({edited_image_url})")
            
            except Exception as e:
                st.error(f"Error: {e}")
