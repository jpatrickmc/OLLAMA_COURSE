# Title: Make a Video Describer
#
# Description:
# This project creates a "Video Describer" that watches a video and tells you what happens in it.
#
# The Workflow:
# 1. User uploads a video (Streamlit).
# 2. We extract frames from the video (OpenCV), e.g., one image every 4 seconds.
# 3. We ask a Vision Model (Llava) to describe each frame.
# 4. We collect all descriptions into one text block.
# 5. We ask a Language Model (Llama 2) to summarize into one coherent story.
#
# Installation:
# pip install opencv-python ollama streamlit
#
# How to run:
# streamlit run video_describer.py

import os
import tempfile

import cv2
import ollama
import streamlit as st


# --- Function 1: Extract Frames ---
# Extract one frame every 4 seconds and return saved frame paths.
def video_to_frames(video_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise RuntimeError("Error: Could not open video.")

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = max(1, int(fps * 4))

    frame_count = 0
    saved_frame_count = 0
    frame_paths = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            filename = f"frame_{saved_frame_count}.jpg"
            cv2.imwrite(filename, frame)
            frame_paths.append(filename)
            saved_frame_count += 1

        frame_count += 1

    cap.release()
    return frame_paths


st.title("Video Describer")

if "last_file_name" not in st.session_state:
    st.session_state.last_file_name = None
if "video_summary" not in st.session_state:
    st.session_state.video_summary = None
# Streamlit's file_uploader keeps widget state by key; rotating the key clears selection.
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0


def reset_app_state():
    # Reset all user-facing results and force a clean uploader widget.
    st.session_state.last_file_name = None
    st.session_state.video_summary = None
    st.session_state.uploader_key += 1
    st.rerun()

uploaded_file = st.file_uploader(
    "Choose a video", type=["mp4"], key=f"video_uploader_{st.session_state.uploader_key}"
)

if uploaded_file is not None:
    # New upload invalidates prior summary so users do not see stale output.
    if st.session_state.last_file_name != uploaded_file.name:
        st.session_state.last_file_name = uploaded_file.name
        st.session_state.video_summary = None

    col1, col2 = st.columns(2)
    describe_clicked = col1.button("Describe Video")
    reset_clicked = col2.button("Reset")

    if reset_clicked:
        reset_app_state()

    if describe_clicked:
        frames = []
        video_path = None
        try:
            print(f"Starting analysis for uploaded file: {uploaded_file.name}")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
                temp_video.write(uploaded_file.getbuffer())
                video_path = temp_video.name

            with st.spinner("Extracting frames and analyzing video..."):
                frames = video_to_frames(video_path)
                print(f"Extracted {len(frames)} frame(s) for analysis")

                descriptions = ""
                st.markdown("### Frame-by-frame breakdown")
                for idx, frame_file in enumerate(frames, start=1):
                    print(f"Analyzing frame {idx}/{len(frames)}: {frame_file}")
                    response = ollama.chat(
                        model="llava:7b",
                        messages=[
                            {
                                "role": "user",
                                "content": "Describe the image with one sentence.",
                                "images": [frame_file],
                            }
                        ],
                    )
                    frame_description = response["message"]["content"]
                    print(f"Frame {idx} description: {frame_description}")

                    image = cv2.imread(frame_file)
                    st.image(image, caption=f"Frame {idx}: {frame_file}", width=700)
                    st.markdown(f"#### Description: {frame_description}")

                    descriptions += f"\n{frame_description}\n"

                prompt = (
                    "Write a general explanation about what is going on in the video by "
                    "using the following descriptions of the video frames.\n"
                    f"{descriptions}"
                )

                answer = ollama.generate(model="llama2", prompt=prompt)
                st.session_state.video_summary = answer["response"]
                print("Video summary generated successfully")

        except Exception as exc:
            print(f"Video analysis failed: {exc}")
            st.error(f"Failed to describe video: {exc}")

        finally:
            # Always delete temporary artifacts, even if model inference fails.
            if video_path and os.path.exists(video_path):
                os.remove(video_path)
            for frame_file in frames:
                if os.path.exists(frame_file):
                    os.remove(frame_file)

    if st.session_state.video_summary:
        st.markdown("### Description of the video")
        st.markdown(st.session_state.video_summary)
else:
    st.session_state.last_file_name = None
    st.session_state.video_summary = None
