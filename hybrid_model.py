import os
import cv2
from ultralytics import YOLO
from ocr_engine import extract_digit
import re

# load model
model = YOLO("best.pt")

dataset_path = r"C:\Users\SANIKA\Downloads\archive (20)\seven_plastics"

correct = 0
total = 0

for folder in os.listdir(dataset_path):
    folder_path = os.path.join(dataset_path, folder)

    match = re.findall(r'\d+', folder)
    if not match:
        continue

    true_label = match[0]

    # skip no plastic
    if true_label == '8':
        continue

    for file in os.listdir(folder_path):

        if not file.lower().endswith(('.jpg', '.png', '.jpeg')):
            continue

        img_path = os.path.join(folder_path, file)
        img = cv2.imread(img_path)

        if img is None:
            continue

        # OCR first
        ocr_result = extract_digit(img)

        # MODEL prediction
        result = model(img)[0]
        model_pred = result.names[result.probs.top1]
        model_digit = re.findall(r'\d', model_pred)[0]

        # HYBRID LOGIC
        if ocr_result is not None:
            final_pred = ocr_result
        else:
            final_pred = model_digit

        print(f"{file} → OCR: {ocr_result}, Model: {model_digit}, Final: {final_pred}, Actual: {true_label}")

        if final_pred == true_label:
            correct += 1

        total += 1

# accuracy
if total > 0:
    print("\nFinal Accuracy:", (correct/total)*100, "%")
else:
    print("No images processed")