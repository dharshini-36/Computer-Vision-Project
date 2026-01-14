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
    - Stroke & Fill colors
    - Adjustable brush thickness

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

    stroke_color = st.sidebar.color_picker("Stroke Color", "#000000")
    fill_color = st.sidebar.color_picker("Fill Color", "#ffffff")

    stroke_width = st.sidebar.slider("Brush Size", 1, 20, 3)

    # Convert fill color to RGBA
    fill_color_rgba = f"rgba({int(fill_color[1:3],16)}, {int(fill_color[3:5],16)}, {int(fill_color[5:7],16)}, 1)"

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
        fill_color=fill_color_rgba if tool in ["rect", "circle"] else "rgba(0,0,0,0)",
        stroke_width=stroke_width,
        stroke_color=stroke_color,
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
