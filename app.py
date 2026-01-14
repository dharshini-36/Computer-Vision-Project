import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import datetime
from io import BytesIO

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Painting App", layout="centered")

# ---------------- SESSION STATE ----------------
if "page" not in st.session_state:
    st.session_state.page = "instructions"

def go_to_painting():
    st.session_state.page = "paint"

def go_to_instructions():
    st.session_state.page = "instructions"

# ---------------- INSTRUCTIONS PAGE ----------------
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
        go_to_painting()

# ---------------- PAINTING PAGE ----------------
elif st.session_state.page == "paint":
    st.title("🖌️ Streamlit Painting App")

    # -------- SIDEBAR CONTROLS --------
    st.sidebar.header("Controls")

    tool = st.sidebar.selectbox(
        "Select Drawing Tool",
        ("freedraw", "line", "rect", "circle")
    )

    color = st.sidebar.color_picker("Choose Color", "#000000")
    stroke_width = st.sidebar.slider("Brush Size", 1, 20, 3)

    # -------- HIDE CANVAS TOOLBAR --------
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

    # -------- CANVAS --------
    canvas_result = st_canvas(
        fill_color="rgba(0, 0, 0, 0)",
        stroke_width=stroke_width,
        stroke_color=color,
        background_color="#ffffff",
        drawing_mode=tool,
        height=400,
        width=600,
        key="canvas"
    )

    # -------- DOWNLOAD --------
    if canvas_result.image_data is not None:
        img = Image.fromarray(
            canvas_result.image_data.astype("uint8"),
            "RGBA"
        )

        buffer = BytesIO()
        img.save(buffer, format="PNG")

        filename = (
            "painting_"
            + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            + ".png"
        )

        st.download_button(
            label="⬇️ Download Painting",
            data=buffer.getvalue(),
            file_name=filename,
            mime="image/png"
        )

    # -------- NAVIGATION --------
    if st.button("⬅️ Back to Instructions"):
        go_to_instructions()
