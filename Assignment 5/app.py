import json
import os  # <-- ADDED THIS IMPORT
import urllib.parse
from io import BytesIO
import requests
import streamlit as st
from gtts import gTTS
from google import genai
from google.genai import types

def get_gemini_client():
    """Fetches key securely from Streamlit secrets or system environment with auto-retry."""
    api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("🔑 API Key Missing! Please add GEMINI_API_KEY to secrets.toml or environment variables.")
        st.stop()
        
    # Enable automatic retries for transient server errors (503, 429, 500)
    retry_config = types.HttpOptions(
        retry_options=types.HttpRetryOptions(
            attempts=5,
            initial_delay=2.0,
            max_delay=30.0,
            http_status_codes=[408, 429, 500, 502, 503, 504]
        )
    )
    
    return genai.Client(api_key=api_key, http_options=retry_config)

# Set up Streamlit Page Configuration
st.set_page_config(
    page_title="Visual Novel Engine", page_icon="🎭", layout="centered"
)

# ==========================================
# PHASE 1: UI & CONFIGURATION
# ==========================================

# Sidebar Configuration
st.sidebar.title("🎮 Story Settings")
genre = st.sidebar.selectbox(
    "Story Genre", ["Cyberpunk", "Dark Fantasy", "Sci-Fi Horror", "Cosmic Mystery"]
)
art_style = st.sidebar.selectbox(
    "Art Style", ["Anime", "Pixel Art", "Digital Oil Painting", "Unreal Engine 5"]
)

if st.sidebar.button("Restart Story"):
    st.session_state.clear()
    st.rerun()

st.title("🎭 Multi-Modal Visual Novel Engine")

# ==========================================
# SYSTEM PROMPT & STATE INITIALIZATION
# ==========================================

SYSTEM_PROMPT = f"""
You are an expert Choose Your Own Adventure visual novel director.
The story genre is '{genre}' and the visual art style is '{art_style}'.

CRITICAL INSTRUCTION: You MUST ALWAYS reply strictly with a valid JSON object. 
Do not include any text before or after the JSON block. Do not wrap it in triple backticks unless necessary.

The JSON structure must be EXACTLY:
{{
  "story_text": "A brief, compelling narrative paragraph (2-4 sentences).",
  "image_prompt": "A detailed, descriptive image prompt reflecting the scene in {art_style} style, highly detailed.",
  "options": [
    "Option 1 description",
    "Option 2 description",
    "Option 3 description"
  ]
}}
"""

# Initialize Session State
if "chat" not in st.session_state:
    try:
        client = get_gemini_client()
        st.session_state.chat = client.chats.create(
            model="gemini-3.1-flash-lite",
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                response_mime_type="application/json",  # Force structured JSON response
            ),
        )
    except Exception as e:
        st.error(
            f"Failed to initialize Gemini Client. Check your API key. Error: {e}"
        )
        st.stop()

if "history" not in st.session_state:
    st.session_state.history = []

if "current_node" not in st.session_state:
    st.session_state.current_node = None

# ==========================================
# HELPER FUNCTIONS
# ==========================================


def fetch_pollinations_image(prompt: str):
    """Fetch an image from Pollinations API with error handling."""
    try:
        encoded_prompt = urllib.parse.quote(f"{prompt}, {art_style} style")
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=450&seed=42&nologo=true"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.content
        else:
            st.toast("⚠️ Image server busy. Continuing story without visual...")
            return None
    except Exception:
        st.toast("⚠️ Network error fetching image. Skipping visual...")
        return None


def generate_tts_audio(text: str):
    """Convert story text into speech audio bytes using gTTS."""
    try:
        tts = gTTS(text=text, lang="en", slow=False)
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp
    except Exception:
        st.toast("⚠️ Speech synthesis unavailable...")
        return None


def process_turn(user_input: str = None):
    """Send user action to Gemini, parse JSON, handle multimedia, and update state."""
    with st.spinner("Directing the next scene..."):
        try:
            prompt = user_input if user_input else "Begin the story."
            response = st.session_state.chat.send_message(prompt)

            # PHASE 2: JSON Parsing
            data = json.loads(response.text)

            # Validate expected JSON fields
            story_text = data.get("story_text", "The story continues...")
            image_prompt = data.get("image_prompt", f"A scene from {genre}")
            options = data.get("options", ["Continue..."])

            # PHASE 4: Multi-Media Processing
            image_bytes = fetch_pollinations_image(image_prompt)
            audio_bytes = generate_tts_audio(story_text)

            node_data = {
                "story_text": story_text,
                "image_bytes": image_bytes,
                "audio_bytes": audio_bytes,
                "options": options,
            }

            # Save previous node to history if it exists
            if st.session_state.current_node:
                st.session_state.history.append(st.session_state.current_node)

            st.session_state.current_node = node_data

        except json.JSONDecodeError:
            st.toast("⚠️ Story generation payload malformed. Retrying...")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")


# ==========================================
# RENDER LOOP & PHASE 3: DYNAMIC UI
# ==========================================

# Initial Kickoff trigger
if st.session_state.current_node is None:
    process_turn()

# Render Chat/Story History
for idx, scene in enumerate(st.session_state.history):
    with st.chat_message("assistant"):
        if scene["image_bytes"]:
            st.image(
                scene["image_bytes"], use_container_width=True
            )
        st.write(scene["story_text"])

# Render Current Active Scene
if st.session_state.current_node:
    current = st.session_state.current_node
    with st.chat_message("assistant"):
        if current["image_bytes"]:
            st.image(
                current["image_bytes"], use_container_width=True
            )

        st.markdown(f"### {current['story_text']}")

        if current["audio_bytes"]:
            st.audio(current["audio_bytes"], format="audio/mp3", autoplay=True)

    st.write("---")
    st.subheader("What do you do next?")

    # Dynamic Choice Buttons
    cols = st.columns(len(current["options"]))
    for index, option in enumerate(current["options"]):
        with cols[index]:
            if st.button(option, key=f"btn_{index}_{hash(option)}"):
                process_turn(option)
                st.rerun()