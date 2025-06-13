import streamlit as st
import cv2
import numpy as np
from ultralytics import YOLO
import tempfile
import os
import time

@st.cache_resource
def load_model():
    try:
        return YOLO('yolov8n.pt')
    except Exception as e:
        st.error(f"Failed to load YOLO model: {str(e)}")
        return None

model = load_model()
if model is None:
    st.stop()

st.title("YOLOv8 Object Detection")

st.sidebar.header("Input Options")
input_option = st.sidebar.radio("Choose input source:", ("Video", "Webcam"))

if 'webcam_active' not in st.session_state:
    st.session_state.webcam_active = False

def process_frame(frame):
    try:
        results = model.predict(source=frame, conf=0.25, show=False)
        annotated_frame = results[0].plot()
        return annotated_frame
    except Exception as e:
        st.error(f"Error processing frame: {str(e)}")
        return frame

if input_option == "Video":
    uploaded_file = st.file_uploader("Upload a video", type=["mp4", "avi", "mov"])
    if uploaded_file is not None:
        try:
            tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
            tfile.write(uploaded_file.read())
            tfile.close()

            cap = cv2.VideoCapture(tfile.name)
            if not cap.isOpened():
                st.error("Failed to load video. Please upload a valid video file.")
                os.unlink(tfile.name)
                st.stop()

            fps = int(cap.get(cv2.CAP_PROP_FPS))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            output_path = "annotated_video.mp4"
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

            stframe = st.empty()
            frame_count = 0
            progress_bar = st.progress(0)

            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                annotated_frame = process_frame(frame)
                out.write(annotated_frame)
                
                if frame_count % 10 == 0:
                    stframe.image(annotated_frame, channels="BGR", caption=f"Frame {frame_count + 1}")
                    progress_bar.progress((frame_count + 1) / total_frames)
                
                frame_count += 1

            cap.release()
            out.release()
            
            st.success(f"Video processed successfully! Total frames: {frame_count}")
            
            if os.path.exists(output_path):
                with open(output_path, "rb") as file:
                    st.download_button(
                        label="Download Annotated Video",
                        data=file,
                        file_name=output_path,
                        mime="video/mp4"
                    )
                os.unlink(output_path)
            else:
                st.error("Failed to save annotated video.")

        except Exception as e:
            st.error(f"Error processing video: {str(e)}")
        finally:
            if 'tfile' in locals():
                os.unlink(tfile.name)
    else:
        st.info("Please upload a video to proceed.")

elif input_option == "Webcam":
    if st.button("Start Webcam"):
        st.session_state.webcam_active = True
    if st.session_state.webcam_active and st.button("Stop Webcam"):
        st.session_state.webcam_active = False

    if st.session_state.webcam_active:
        try:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                st.error("Could not access webcam. Please ensure it is connected and accessible.")
                st.session_state.webcam_active = False
                st.stop()
            
            stframe = st.empty()
            
            frame_skip = 2
            frame_count = 0

            while st.session_state.webcam_active:
                ret, frame = cap.read()
                if not ret:
                    st.error("Failed to capture video frame.")
                    break
                
                if frame_count % frame_skip == 0:
                    annotated_frame = process_frame(frame)
                    stframe.image(annotated_frame, channels="BGR", use_column_width=True)
                
                frame_count += 1
                
                time.sleep(0.03)
            
            cap.release()
        except Exception as e:
            st.error(f"Webcam error: {str(e)}")
            st.session_state.webcam_active = False
        finally:
            if 'cap' in locals() and cap.isOpened():
                cap.release()
    else:
        st.info("Click 'Start Webcam' to begin video capture.")