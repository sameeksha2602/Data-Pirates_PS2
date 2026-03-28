import streamlit as st
import numpy as np
from PIL import Image
from ultralytics import YOLO

st.set_page_config(page_title="Smart Waste Classifier", layout="centered")

st.title("Smart Waste Detection System")

# Load YOLO model
@st.cache_resource
def load_model():
    model = YOLO("models/best.pt")
    return model

model = load_model()

# Disposal instructions
instructions = {

"plastic": """
Dustbin: Dry Waste (Blue Bin)

Steps:
1. Empty the container
2. Rinse lightly if dirty
3. Remove cap if possible
4. Crush bottle to save space
""",

"paper": """
Dustbin: Dry Waste (Blue Bin)

Steps:
1. Ensure paper is dry
2. Remove plastic covers
3. Stack or fold large sheets
""",

"cardboard": """
Dustbin: Dry Waste (Blue Bin)

Steps:
1. Remove tape or plastic
2. Flatten the cardboard
3. Ensure it is dry
""",

"glass": """
Dustbin: Dry Waste (Blue Bin)

Steps:
1. Empty the bottle
2. Remove caps
3. Place carefully to avoid breakage
""",

"trash": """
Dustbin: General Waste (Green Bin)

Steps:
1. Ensure it cannot be recycled
2. Place directly in green bin
"""
}

# Bin color mapping
bin_color = {
"plastic": "blue",
"paper": "blue",
"cardboard": "blue",
"glass": "blue",
"trash": "green"
}

option = st.radio(
"Choose Input Method",
["Upload Image", "Capture from Webcam"]
)

def run_detection(image):

    results = model(image)

    result = results[0]

    detected_class = None
    annotated_frame = image

    # Classification model
    if result.probs is not None:
        class_id = int(result.probs.top1)
        detected_class = result.names[class_id]

    # Detection model
    elif result.boxes is not None and len(result.boxes) > 0:
        annotated_frame = result.plot()
        class_id = int(result.boxes.cls[0])
        detected_class = result.names[class_id]

    return annotated_frame, detected_class


def show_bin_card(class_name):

    color = bin_color.get(class_name, "gray")

    if color == "blue":
        st.markdown(
        """
        ### Recommended Bin
        <div style="background-color:#2196F3;padding:15px;border-radius:10px;color:white">
        <h3>BLUE BIN</h3>
        Dry / Recyclable Waste
        </div>
        """,
        unsafe_allow_html=True
        )

    elif color == "green":
        st.markdown(
        """
        ### Recommended Bin
        <div style="background-color:#4CAF50;padding:15px;border-radius:10px;color:white">
        <h3>GREEN BIN</h3>
        General Waste
        </div>
        """,
        unsafe_allow_html=True
        )


# Upload Image
if option == "Upload Image":

    uploaded_file = st.file_uploader("Upload an image", type=["jpg","jpeg","png"])

    if uploaded_file is not None:

        image = Image.open(uploaded_file)
        image_np = np.array(image)

        st.image(image, caption="Original Image", width="stretch")

        if st.button("Run Detection"):

            result_img, detected_class = run_detection(image_np)

            st.image(result_img, caption="Detection Result", width="stretch")

            if detected_class:

                st.subheader(f"Detected Object: {detected_class}")

                show_bin_card(detected_class)

                st.subheader("Disposal Instructions")

                st.write(instructions.get(detected_class, "No instructions available"))


# Webcam Capture
if option == "Capture from Webcam":

    camera_image = st.camera_input("Capture Image")

    if camera_image is not None:

        image = Image.open(camera_image)
        image_np = np.array(image)

        st.image(image, caption="Captured Image", width="stretch")

        if st.button("Run Detection"):

            result_img, detected_class = run_detection(image_np)

            st.image(result_img, caption="Detection Result", width="stretch")

            if detected_class:

                st.subheader(f"Detected Object: {detected_class}")

                show_bin_card(detected_class)

                st.subheader("Disposal Instructions")

                st.write(instructions.get(detected_class, "No instructions available"))
