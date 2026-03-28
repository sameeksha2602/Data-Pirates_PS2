Smart Waste Detection System
Overview

The Smart Waste Detection System is an AI-based application developed to improve waste segregation by automatically identifying waste types and providing appropriate disposal guidance.
Dataset links:https://drive.google.com/drive/folders/1IZMXkMT8puUf3Zej2oZ_8A_Jkds33Tnw?usp=sharing
              https://drive.google.com/drive/folders/1yuGDoMEkYD8WFKGxV6bv-GNN3tQ9OLyw?usp=sharing

Improper waste segregation leads to inefficient recycling and increased landfill waste. This system addresses this issue using a hybrid approach that combines deep learning and optical character recognition (OCR) to enhance classification accuracy.

Key Features
Automated waste classification using a YOLOv8-based model
Resin code detection using OCR for plastic identification
Hybrid decision mechanism (OCR prioritization with model fallback)
Support for both image upload and live camera-based detection
Recommendation of appropriate disposal bins
Step-by-step disposal instructions
Gamification system with carbon points and badges
User-friendly interface built with Streamlit
Technologies Used
Python
YOLOv8 (Ultralytics) for image classification
OpenCV for image preprocessing
Tesseract OCR for text extraction
Streamlit for web application interface
NumPy and PIL for image handling
System Workflow
Input (Upload Image / Live Camera)
          ↓
Image Preprocessing (OpenCV)
          ↓
OCR Detection (Resin Code)
          ↓
YOLOv8 Model Prediction
          ↓
Hybrid Decision Logic
          ↓
Waste Classification
          ↓
Bin Recommendation and Instructions
          ↓
Gamification Feedback
| Score Range | Badge                 |
| ----------- | --------------------- |
| 0–9         | ♻️ Getting Started    |
| 10–29       | 🌱 Beginner Recycler  |
| 30–49       | 🌟 Eco Warrior        |
| 50+         | 🏆 Recycling Champion |

Working Principle
The user provides input either by uploading an image or capturing it using a live camera feed.
The image is preprocessed using OpenCV to enhance quality and improve detection accuracy.
OCR is applied to detect resin codes if they are visible on the object.
The YOLOv8 model analyzes visual features such as shape, texture, and material type.
If OCR successfully detects a resin code, it is prioritized; otherwise, the model’s prediction is used.
The system displays the waste category, recommended disposal bin, and step-by-step instructions.
Users receive carbon points and badges based on their interactions.
Output Screenshots:
<img width="1600" height="782" alt="image" src="https://github.com/user-attachments/assets/07743345-bbe1-454a-bf35-36ec918a7188" />
<img width="1600" height="724" alt="image" src="https://github.com/user-attachments/assets/fd855d6f-efb2-4e95-8777-1509ea07f58c" />
<img width="1600" height="733" alt="image" src="https://github.com/user-attachments/assets/5e7a0eee-cc79-4be6-80eb-b674fa9c24d8" />
<img width="1600" height="729" alt="image" src="https://github.com/user-attachments/assets/215fcb7b-ede8-427b-8e8a-5dfd5f0c00b9" />
<img width="1600" height="721" alt="image" src="https://github.com/user-attachments/assets/4ebe1b39-e076-4b89-a263-b34886acd3a8" />
<img width="1600" height="718" alt="image" src="https://github.com/user-attachments/assets/0a32b875-5473-4395-8c77-ac7bcca4db8d" />
<img width="1600" height="701" alt="image" src="https://github.com/user-attachments/assets/28f9db4c-1e42-496e-a529-6af8f60a7b86" />


accuracy for plastic seregation:
<img width="1600" height="897" alt="image" src="https://github.com/user-attachments/assets/0f04bf8a-9295-4e4c-811c-8019890da2f2" />

video demonstration:
https://drive.google.com/file/d/1qd5hQdhPAdSG1zfYiubbXIp61ZyVLbAh/view?usp=sharing

