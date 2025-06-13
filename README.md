YOLOv8 Object Detection with Streamlit
This project is a Streamlit web application that uses the YOLOv8 model to perform real-time object detection on videos or webcam streams. It allows users to upload a video file or use their webcam to detect objects and download the annotated video output.
Features

Object detection using the YOLOv8 nano model (yolov8n.pt).
Supports video file uploads (.mp4, .avi, .mov).
Real-time webcam streaming with object detection.
Downloadable annotated video output.
User-friendly interface with progress bar for video processing.

Requirements

Python 3.8 or later
Dependencies:
streamlit
opencv-python
numpy
ultralytics



Installation

Clone or Download the Repository:Download the project files or clone the repository to your local machine.

Install Dependencies:Open a terminal and install the required Python packages:
pip install streamlit opencv-python numpy ultralytics


Download YOLOv8 Model:The yolov8n.pt model file will be automatically downloaded by the Ultralytics library on first run. Ensure an internet connection, or manually download yolov8n.pt from the Ultralytics GitHub releases and place it in the project directory.


Usage

Run the Application:Navigate to the project directory and start the Streamlit server:
streamlit run assignment_18.py

This opens the app in your default browser at http://localhost:8501.

Video Mode:

Select "Video" from the sidebar.
Upload a video file (.mp4, .avi, or .mov).
The app processes the video, displays frames with detected objects, and provides a download link for the annotated video.


Webcam Mode:

Select "Webcam" from the sidebar.
Click "Start Webcam" and grant camera permissions.
View real-time object detection.
Click "Stop Webcam" to end the stream.



Troubleshooting

Webcam Issues:

If the webcam fails to open, ensure it’s connected and not used by another application.
Try changing the camera index in cv2.VideoCapture(0) to 1 or 2.
On macOS/Linux, verify camera permissions.


Video Processing Errors:

Ensure uploaded videos are in a supported format.
If the annotated video fails to save, try changing the codec in the script (e.g., fourcc = cv2.VideoWriter_fourcc(*'H264')).


Model Loading Errors:

Verify that yolov8n.pt is in the project directory or accessible online.
Check your internet connection for automatic model download.


Performance Issues:

For slow performance, ensure you’re using a GPU for YOLO inference (if available).
Increase frame_skip in the webcam section or reduce video resolution.



Notes

The app uses the YOLOv8 nano model for lightweight performance. For better accuracy, consider using larger models like yolov8s.pt or yolov8m.pt (update the script accordingly).
Webcam streaming may lag in the browser due to Streamlit’s reactive model. For better performance, consider using streamlit-webrtc for webcam handling.

License
This project is for educational purposes and uses open-source libraries. Ensure compliance with the licenses of Streamlit, OpenCV, NumPy, and Ultralytics YOLOv8.
