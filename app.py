import streamlit as st
import cv2
import numpy as np
from ultralytics import YOLO
import pytesseract
import re
from PIL import Image

# ----------- TESSERACT PATH -----------
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ----------- LOAD MODEL -----------
model = YOLO("best.pt")

# ----------- KNOWLEDGE BASE -----------
plastic_info = {
    "1": {"name": "PET (Polyethylene Terephthalate)", "bin": "Blue Bin (Recyclable)", "instruction": "Wash before recycling. Common in water bottles."},
    "2": {"name": "HDPE (High-Density Polyethylene)", "bin": "Blue Bin (Recyclable)", "instruction": "Rinse and recycle. Used in milk containers."},
    "3": {"name": "PVC (Polyvinyl Chloride)", "bin": "General Waste", "instruction": "Not easily recyclable. Avoid if possible."},
    "4": {"name": "LDPE (Low-Density Polyethylene)", "bin": "Special Collection", "instruction": "Recycle at designated centers."},
    "5": {"name": "PP (Polypropylene)", "bin": "Blue Bin (Recyclable)", "instruction": "Clean before recycling. Used in food containers."},
    "6": {"name": "PS (Polystyrene)", "bin": "General Waste", "instruction": "Not recyclable in most areas."},
    "7": {"name": "Other Plastics", "bin": "General Waste", "instruction": "Difficult to recycle. Dispose carefully."}
}

# ----------- GAMIFICATION INIT -----------
if "score" not in st.session_state:
    st.session_state.score = 0

if "item_count" not in st.session_state:
    st.session_state.item_count = 0

# ----------- GAMIFICATION LOGIC -----------
def get_points(pred):
    if pred in ["1", "2", "5"]:
        return 5
    elif pred in ["4"]:
        return 3
    else:
        return 1

def get_badge(score):
    if score >= 50:
        return "🏆 Recycling Champion"
    elif score >= 30:
        return "🌟 Eco Warrior"
    elif score >= 10:
        return "🌱 Beginner Recycler"
    else:
        return "♻️ Getting Started"

# ----------- OCR FUNCTION -----------
def extract_digit(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.convertScaleAbs(gray, alpha=2, beta=50)
    gray = cv2.GaussianBlur(gray, (5,5), 0)

    h, w = gray.shape
    crop = gray[int(h*0.4):int(h*0.8), int(w*0.3):int(w*0.7)]

    thresh = cv2.adaptiveThreshold(
        crop, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11, 2
    )

    thresh = cv2.resize(thresh, None, fx=2, fy=2)

    text = pytesseract.image_to_string(
        thresh,
        config='--psm 10 -c tessedit_char_whitelist=1234567'
    )

    digit = re.findall(r'\d', text)
    return digit[0] if digit else None

# ----------- PREDICTION FUNCTION -----------
def predict_image(image):
    img = np.array(image)

    ocr_result = extract_digit(img)

    result = model(img)[0]
    model_pred = result.names[result.probs.top1]
    model_digit = re.findall(r'\d', model_pred)[0]

    if ocr_result is not None:
        final_pred = ocr_result
        source = "OCR"
    else:
        final_pred = model_digit
        source = "Model"

    return final_pred, source

# ----------- UI -----------
st.title("♻️ Smart Waste Detection System")

# ----------- IMAGE UPLOAD -----------
st.header(" Upload Image")

uploaded_file = st.file_uploader("Upload waste image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    pred, source = predict_image(image)

    st.success(f"🔢 Resin Code: {pred}")
    st.info(f"Detected by: {source}")

    info = plastic_info.get(pred)

    if info:
        st.subheader(f"♻️ Category: {info['name']}")
        st.write(f"🗑️ Bin: {info['bin']}")
        st.write(f"📋 Instruction: {info['instruction']}")

    # ----------- GAMIFICATION UPDATE -----------
    points = get_points(pred)
    st.session_state.score += points
    st.session_state.item_count += 1

    st.success(f"🌱 +{points} Carbon Points Earned!")

    # ----------- SCOREBOARD -----------
    st.subheader("📊 Your Eco Score")
    st.write(f"♻️ Items Sorted: {st.session_state.item_count}")
    st.write(f"🌱 Total Carbon Points: {st.session_state.score}")

    badge = get_badge(st.session_state.score)
    st.success(f"🏆 Badge: {badge}")