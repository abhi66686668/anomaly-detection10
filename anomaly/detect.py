from ultralytics import YOLO
import cv2
import os
import csv
from collections import defaultdict
from anomaly import calculate_distance

model = YOLO("yolov8n.pt")

files = os.listdir("upload")

if not files:
    print("No video found in upload folder")
    exit()

video_path = os.path.join("upload", files[0])

cap = cv2.VideoCapture(video_path)

fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

os.makedirs("output", exist_ok=True)

out = cv2.VideoWriter(
    "output/result.mp4",
    cv2.VideoWriter_fourcc(*'mp4v'),
    fps,
    (width, height)
)

csv_file = open(
    "output/report.csv",
    "w",
    newline=""
)

writer = csv.writer(csv_file)
writer.writerow(["PersonID", "AlertType"])

positions = {}
stationary_frames = defaultdict(int)
alert_sent = set()

frame_count = 0

while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame_count += 1

    results = model.track(
        frame,
        persist=True,
        classes=[0],
        conf=0.60,
        tracker="bytetrack.yaml"
    )

    annotated = frame.copy()

    if (
        results[0].boxes is not None and
        results[0].boxes.id is not None
    ):

        boxes = results[0].boxes.xyxy.cpu().numpy()
        ids = results[0].boxes.id.cpu().numpy()

        for box, track_id in zip(boxes, ids):

            x1, y1, x2, y2 = map(int, box)

            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            current_pos = (center_x, center_y)

            track_id = int(track_id)

            cv2.rectangle(
                annotated,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            cv2.putText(
                annotated,
                f"ID:{track_id}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

            if track_id in positions:

                distance = calculate_distance(
                    positions[track_id],
                    current_pos
                )

                # Running Detection
                if distance > 20:

                    cv2.putText(
                        annotated,
                        "SUSPICIOUS ACTIVITY",
                        (x1, y1 - 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0, 0, 255),
                        2
                    )

                    key = f"{track_id}_RUNNING"

                    if key not in alert_sent:

                        writer.writerow([
                            track_id,
                            "RUNNING"
                        ])

                        alert_sent.add(key)

                # Loitering Detection
                if distance < 2:
                    stationary_frames[track_id] += 1
                else:
                    stationary_frames[track_id] = 0

                if stationary_frames[track_id] > fps * 5:

                    cv2.putText(
                        annotated,
                        "LOITERING ALERT",
                        (x1, y1 - 70),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (255, 0, 0),
                        2
                    )

                    key = f"{track_id}_LOITERING"

                    if key not in alert_sent:

                        writer.writerow([
                            track_id,
                            "LOITERING"
                        ])

                        alert_sent.add(key)

            positions[track_id] = current_pos

    out.write(annotated)

cap.release()
out.release()
csv_file.close()

print("Detection Complete")
print("Video Saved -> output/result.mp4")
print("Report Saved -> output/report.csv")