import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import re
import random
import traceback

load_dotenv()
st.title("🖼️GenAI Playground: Image, Caption & Video Summarizer ✨")

client = genai.Client()

# Session state for history & prompt management
if "messages" not in st.session_state:
    st.session_state.messages = []
if "generated_images" not in st.session_state:
    st.session_state.generated_images = []
if "user_prompt" not in st.session_state:
    st.session_state.user_prompt = ""  # key for image generator

# --- Image Generator ---
st.header("🎨 AI Image Generator")
prompt_examples = [
    "A futuristic cityscape at sunset.",
    "Cats wearing astronaut suits on the moon.",
    "An impressionist-style forest near a river."
]

def set_random_prompt():
    st.session_state.user_prompt = random.choice(prompt_examples)

col1, col2 = st.columns([3, 1])

with col1:
    user_prompt = st.text_input(
        "Describe the image you want to generate:",
        value=st.session_state.user_prompt,
        key="user_prompt"
    )
with col2:
    st.button("Surprise Me", on_click=set_random_prompt)

st.markdown("**Examples:**")
for eg in prompt_examples:
    st.write(f"• _{eg}_")

if st.button("Generate Image"):
    if not st.session_state.user_prompt:
        st.warning("⚠️ Please enter a prompt!")
    else:
        try:
            with st.spinner("🖌️ Generating image..."):
                response = client.models.generate_content(
                    model="gemini-2.0-flash-exp-image-generation",
                    contents=st.session_state.user_prompt,
                    config=types.GenerateContentConfig(
                        response_modalities=['Text', 'Image']
                    )
                )
            st.subheader("🖼️ Generated Image")
            for part in response.candidates[0].content.parts:
                if part.text is not None:
                    st.write(part.text)
                elif part.inline_data is not None:
                    image = Image.open(BytesIO((part.inline_data.data)))
                    st.image(image)
                    # Save to session history
                    st.session_state.generated_images.append(image)
                    # Download button for this image
                    buffered = BytesIO()
                    image.save(buffered, format="PNG")
                    st.download_button(
                        label="Download Image",
                        data=buffered.getvalue(),
                        file_name="generated_image.png",
                        mime="image/png"
                    )
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            with st.expander("See error details"):
                st.write(traceback.format_exc())

# Gallery of generated images in session
if st.session_state.generated_images:
    st.subheader("🖼️ Image History (Current Session)")
    for idx, image in enumerate(st.session_state.generated_images):
        st.image(image, caption=f"Generated Image {idx+1}")
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        st.download_button(
            label=f"Download Image {idx+1}",
            data=buffered.getvalue(),
            file_name=f"generated_image_{idx+1}.png",
            mime="image/png"
        )

# --- Image Caption Generator ---
st.header("📝 AI Image Caption Generator")
uploaded_image = st.file_uploader("Upload an image for caption generation:", type=["png", "jpg", "jpeg"])

style_options = ["Crisp & Witty", "Formal", "Poetic", "Funny"]
selected_style = st.selectbox("Select caption style:", style_options, key="style_caption")
prompt_map = {
    "Crisp & Witty": "Be as crisp and witty as possible.",
    "Formal": "Describe the image formally.",
    "Poetic": "Write a poetic caption for the image.",
    "Funny": "Create a humorous caption."
}

if uploaded_image:
    try:
        image = Image.open(uploaded_image)
        st.image(image, caption="📷 Uploaded Image")
        if st.button("Generate Caption"):
            try:
                with st.spinner("✍️ Generating caption..."):
                    custom_prompt = f"Tell about the given image. {prompt_map[selected_style]}"
                    response = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=[custom_prompt, image]
                    )
                st.subheader("📝 Generated Caption")
                st.write(response.text)
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                with st.expander("See error details"):
                    st.write(traceback.format_exc())
    except Exception as e:
        st.error(f"❌ Error with image upload: {str(e)}")

# --- YouTube/Video Summarizer ---
st.header("🎬 AI Video Summarizer")
summary_length = st.slider("Select summary length (words):", 50, 300, 100, step=10)
youtube_url = st.text_input("Paste a YouTube Video URL:")
uploaded_video = st.file_uploader("Or upload a video file (mp4, mov, avi):", type=["mp4", "mov", "avi"])
def is_valid_youtube_url(url):
    pattern = r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.be)\/.+$'
    return re.match(pattern, url)

if st.button("Summarize Video"):
    if youtube_url and not is_valid_youtube_url(youtube_url):
        st.error("❌ Please enter a valid YouTube URL!")
    elif not youtube_url and not uploaded_video:
        st.warning("⚠️ Please provide a YouTube URL or upload a video file!")
    else:
        try:
            my_progress = st.progress(0, text="Starting...")
            with st.spinner("Starting video processing..."):
                my_progress.progress(10, text="Reading video...")
                if youtube_url:
                    video_input = types.Part(
                        file_data=types.FileData(file_uri=youtube_url)
                    )
                else:
                    video_bytes = uploaded_video.read()
                    my_progress.progress(30, text="Uploading video...")
                    video_input = types.Part(
                        inline_data=types.InlineData(
                            mime_type=uploaded_video.type,
                            data=video_bytes
                        )
                    )
                my_progress.progress(70, text="Generating summary...")
                content_prompt = f"Summarize the given video in {summary_length} words"
                response = client.models.generate_content(
                    model='models/gemini-2.0-flash',
                    contents=types.Content(
                        parts=[
                            types.Part(text=content_prompt),
                            video_input
                        ]
                    )
                )
                my_progress.progress(100, text="Done!")

            st.subheader("📝 Video Summary")
            st.write(response.text)
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            with st.expander("See error details"):
                st.write(traceback.format_exc())
