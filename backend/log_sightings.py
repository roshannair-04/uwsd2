import os
from datetime import datetime
import cv2
from ultralytics import YOLO
from backend.database import SessionLocal, Sighting, init_db

# --- Setup ---
session = SessionLocal()
model = YOLO("models/yolov8n-face.pt")


def log_sighting(perp_id, img_path, location="Camera 1"):
    print(f"[SIGHTING] Logging for perp {perp_id}, image={img_path}, location={location}")
    results = model(img_path)

    for i, box in enumerate(results[0].boxes.xyxy):
        x1, y1, x2, y2 = map(int, box)
        img = results[0].orig_img.copy()
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Save cropped/annotated image
        out_path = f"sightings/sighting_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{i}.jpg"
        os.makedirs("sightings", exist_ok=True)
        cv2.imwrite(out_path, img)

        # Log into DB
        sighting = Sighting(
            perp_id=perp_id,
            timestamp=datetime.now(),
            location=location,
            screenshot_path=out_path
        )
        session.add(sighting)

    session.commit()
    print(f"[SIGHTING] Logged {len(results[0].boxes)} detections into DB.")


if __name__ == "__main__":
    # Init DB if first run
    init_db()

    # For now, test with John Doe (id=1)
    log_sighting(1, "bus.jpg", location="Test Run")
