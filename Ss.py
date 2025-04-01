import streamlit as st
import openai
from PIL import Image
import io
import moviepy.editor as mpy
import numpy as np
from io import BytesIO

# Set up OpenAI API key
openai.api_key = "your_openai_api_key"

st.title("AI Image to Video Editor")
st.write("Upload an image and provide a prompt for editing the image to generate a video.")

# Upload an image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    # Get user prompt for image edit
    prompt = st.text_area("Enter your image edit request:")

    if st.button("Generate 15-Second Video") and prompt:
        with st.spinner("Creating video..."):
            # Convert image to bytes
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            
            try:
                # Call OpenAI API for image editing
                response = openai.Image.create_edit(
                    image=img_byte_arr,
                    prompt=prompt,
                    n=1,
                    size="512x512"
                )

                # Edited image URL from OpenAI
                edited_image_url = response['data'][0]['url']
                st.image(edited_image_url, caption="Edited Image", use_column_width=True)

                # Create a video from the image with some basic animations (e.g., zoom)
                def make_frame(t):
                    img = np.array(image)
                    zoom_factor = 1 + 0.05 * t  # Zoom effect over time
                    size = (int(image.width * zoom_factor), int(image.height * zoom_factor))
                    img_resized = image.resize(size)
                    return np.array(img_resized)

                # Create a 15-second video
                video_clip = mpy.VideoClip(make_frame, duration=15)

                # Write the video to a BytesIO object
                video_io = BytesIO()
                video_clip.write_videofile(video_io, codec="libx264", audio=False)
                video_io.seek(0)

                # Provide video download link
                st.write("### Download your video")
                st.video(video_io)
                
            except Exception as e:
                st.error(f"Error: {e}")
