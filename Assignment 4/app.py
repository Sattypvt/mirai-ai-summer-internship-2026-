
import streamlit as st
import requests
import urllib.parse
import random

st.set_page_config(page_title="AI Image Studio", page_icon="🎨")

st.title("🎨 AI Image Studio")
st.write("Generate amazing AI images using Pollinations AI!")

# ---------------- Sidebar ----------------

st.sidebar.header("⚙️ Settings")

art_style = st.sidebar.selectbox(
    "Choose Art Style",
    [
        "Realistic",
        "Anime",
        "Fantasy",
        "Cyberpunk",
        "Oil Painting",
        "Watercolor"
    ]
)

width = st.sidebar.slider("Width", 256, 1024, 512, step=64)
height = st.sidebar.slider("Height", 256, 1024, 512, step=64)

magic_enhance = st.sidebar.checkbox("✨ Enable Magic Enhance")

# ---------------- Prompt ----------------

prompt = st.text_input(
    "Enter your prompt",
    placeholder="A dragon flying over a futuristic city..."
)

# ---------------- Surprise Prompts ----------------

surprise_prompts = [
    "An astronaut riding a horse on Mars",
    "A cyberpunk street food vendor in Tokyo",
    "A dragon reading books inside a library",
    "A futuristic underwater city",
    "A giant panda working as a software engineer"
]

generate = st.button("🎨 Generate Image")
surprise = st.button("🎲 Surprise Me!")

# ---------------- Decide Prompt ----------------

selected_prompt = prompt

if surprise:
    selected_prompt = random.choice(surprise_prompts)
    st.success(f"Surprise Prompt:\n\n{selected_prompt}")

# ---------------- Generate ----------------

if generate or surprise:

    if selected_prompt.strip() == "":
        st.warning("Please enter a prompt.")
        st.stop()

    full_prompt = f"{selected_prompt}, {art_style}"

    # Task 3
    if magic_enhance:
        full_prompt += ", masterpiece, 8k resolution, highly detailed, trending on artstation, unreal engine 5 render"

    encoded_prompt = urllib.parse.quote(full_prompt)

    # Task 1
    url = (
        f"https://image.pollinations.ai/prompt/"
        f"{encoded_prompt}"
        f"?width={width}&height={height}"
    )

    st.subheader("Generated Image")

    st.image(url, use_container_width=True)

    try:
        response = requests.get(url)

        if response.status_code == 200:

            # Task 2
            st.download_button(
                "📥 Download Image",
                data=response.content,
                file_name=f"{art_style.lower()}_image.png",
                mime="image/png"
            )

        else:
            st.error("Failed to download image.")

    except Exception as e:
        st.error(str(e))