# 🎥 Suspicious Activity Detection System

This is a Streamlit-based web application that detects suspicious activities like **Running** and **Loitering** from CCTV footage using YOLOv8 and ByteTrack.

## Features

- **Video Upload**: Upload your CCTV footage directly through the web interface (supports `.mp4`, `.avi`, `.mov`).
- **Running Detection**: Detects abnormal, sudden fast movements (distance-based tracking) and flags them as suspicious activity.
- **Loitering Detection**: Detects if a person remains stationary or in a very confined area for an extended period (over 5 seconds).
- **Video Output processing**: Renders the bounding boxes, tracking IDs, and alert labels directly onto the processed video.
- **Report Generation**: Automatically generates a CSV report (`report.csv`) logging the IDs and types of alerts generated.

## Technology Stack

- **Python**: Core programming language.
- **Streamlit**: For the interactive web interface.
- **Ultralytics YOLOv8**: For real-time person detection.
- **ByteTrack**: For object tracking across frames.
- **OpenCV**: For video processing and drawing bounding boxes.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/abhi66686668/anomaly-detection10.git
   cd anomaly-detection10
   ```

2. **Install the dependencies:**
   Make sure you have Python installed. Install the required libraries:
   ```bash
   pip install streamlit ultralytics opencv-python
   ```

3. **Download YOLO weights (Optional):**
   The project uses `yolov8n.pt`. If it's not present, the ultralytics library will automatically download it on the first run.

## Usage

1. Run the Streamlit application:
   ```bash
   cd anomaly
   streamlit run app.py
   ```

2. Open the URL provided in your terminal (typically `http://localhost:8501`).
3. Upload a CCTV video file.
4. Click on **Detect Anomaly**. The system will process the video and display the results, along with the generated report on the web interface.

## Output

- **`output/result.mp4`**: The annotated video with bounding boxes and alerts.
- **`output/report.csv`**: A spreadsheet logging the Person ID and the Alert Type (RUNNING / LOITERING).
