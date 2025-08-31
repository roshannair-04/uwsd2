import cv2
import numpy as np
from ultralytics import YOLO
from insightface.app import FaceAnalysis
from sklearn.metrics.pairwise import cosine_similarity

# --- Load YOLOv8n-face ---
yolo_model = YOLO("/Users/roshannair/Desktop/RoshTek/uwsd2/models/yolov8n-face.pt")  # Ultralytics face model

# --- Load InsightFace (buffalo_l) ---
face_app = FaceAnalysis(name="buffalo_l")
face_app.prepare(ctx_id=0)  # ctx_id=-1 for CPU, 0 for GPU if available

# --- Load test images ---
img1 = cv2.imread("data/test1.jpg")  # known person
img2 = cv2.imread("data/test2.jpg")  # same or diff person

# --- Run YOLO on img1 ---
results1 = yolo_model(img1)
for box in results1[0].boxes.xyxy:
    x1, y1, x2, y2 = map(int, box)
    face_crop = img1[y1:y2, x1:x2]
    cv2.imwrite("face1.jpg", face_crop)

# --- Run YOLO on img2 ---
results2 = yolo_model(img2)
for box in results2[0].boxes.xyxy:
    x1, y1, x2, y2 = map(int, box)
    face_crop = img2[y1:y2, x1:x2]
    cv2.imwrite("face2.jpg", face_crop)

# --- Extract embeddings ---
faces1 = face_app.get(cv2.imread("face1.jpg"))
faces2 = face_app.get(cv2.imread("face2.jpg"))

if faces1 and faces2:
    emb1 = faces1[0].embedding.reshape(1, -1)
    emb2 = faces2[0].embedding.reshape(1, -1)

    # Cosine similarity
    score = cosine_similarity(emb1, emb2)[0][0]
    print(f"Cosine similarity: {score:.4f}")
    if score > 0.35:  # tweak threshold
        print("✅ Same person detected")
    else:
        print("❌ Different persons")
else:
    print("No face detected in one of the images")
