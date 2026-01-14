import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import datetime

# Page config
st.set_page_config(page_title="Painting App", layout="centered")

# Session state for page navigation
if "page" not in st.session_state:
    st.session_state.page = "instructions"

# Function to switch pages safely
def go_to_painting():
    st.session_state.page = "paint"

def go_to_instructions():
    st.session_state.page = "instructions"

# ---------------- INSTRUCTION PAGE ----------------
if st.session_state.page == "instructions":
    st.title("🎨 Painting Application")
    st.subheader("Instructions")

    st.markdown("""
    ### ✏️ Drawing Tools
    - Freehand drawing
    - Line, Rectangle, Circle

    ### 🎨 Colors & Brush
    - Choose any color
    - Adjust brush thickness

    ### 💾 Download
    - Download your painting as an image

    ### ▶️ How to Start
    - Click **Start Painting** to open the canvas
    """)

    if st.button("🚀 Start Painting"):
        go_to_painting()  # Safe page switch

# ---------------- PAINTING PAGE ----------------
elif st.session_state.page == "paint":
    st.title("🖌️ Streamlit Painting App")

    # Sidebar controls
    st.sidebar.header("Controls")

    tool = st.sidebar.selectbox(
        "Select Drawing Tool",
        ("freedraw", "line", "rect", "circle")
    )

    color = st.sidebar.color_picker("Choose Color", "#000000")
    stroke_width = st.sidebar.slider("Brush Size", 1, 20, 3)

    bg_color = "#ffffff"

    # Hide the toolbar
st.markdown(
    """
    <style>
    div[data-testid="stCanvasToolbar"] {
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Canvas
canvas_result = st_canvas(
    fill_color="rgba(0, 0, 0, 0)",
    stroke_width=2,
    stroke_color="#000000",
    background_color="#ffffff",
    height=400,
    width=600,
    key="canvas"
)

    # Download button
    if canvas_result.image_data is not None:
        img = Image.fromarray(canvas_result.image_data.astype("uint8"), "RGBA")

        filename = "painting_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".png"

        st.download_button(
            label="⬇️ Download Painting",
            data=img.tobytes(),
            file_name=filename,
            mime="image/png"
        )

    # Navigation
    if st.button("⬅️ Back to Instructions"):
        go_to_instructions()  # Safe page switch
