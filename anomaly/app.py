import streamlit as st
import os

st.set_page_config(
    page_title="Suspicious Activity Detection",
    page_icon="🎥"
)

st.title("🎥 Suspicious Activity Detection System")

os.makedirs("upload", exist_ok=True)
os.makedirs("output", exist_ok=True)

uploaded_video = st.file_uploader(
    "Upload CCTV Video",
    type=["mp4", "avi", "mov"]
)

if uploaded_video is not None:

    for f in os.listdir("upload"):
        try:
            os.remove(os.path.join("upload", f))
        except:
            pass

    video_path = os.path.join(
        "upload",
        uploaded_video.name
    )

    with open(video_path, "wb") as f:
        f.write(uploaded_video.getbuffer())

    st.success("Video Uploaded Successfully")

    st.video(video_path)

    if st.button("Detect Anomaly"):

        os.system("python detect.py")

        st.success("Detection Completed")

        if os.path.exists("output/result.mp4"):
            st.video("output/result.mp4")

        if os.path.exists("output/report.csv"):

            with open(
                "output/report.csv",
                "r"
            ) as f:

                st.text(f.read())