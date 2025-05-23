import threading

import cv2
import streamlit as st

from streamlit_webrtc import webrtc_streamer

st.set_page_config(page_title="WebRTC Example", layout="wide")
col1, col2 = st.columns(2)

lock = threading.Lock()
img_container = {"img": None}


def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")
    with lock:
        img_container["img"] = img

    return frame

with col1:
    ctx = webrtc_streamer(key="example", video_frame_callback=video_frame_callback, 
                          
                          rtc_configuration={"iceServers": [
                               {"urls": ["turn:relay1.expressturn.com:3478"],
      "username": "efQB4HTEGI9W41QMFK",
      "credential": "W1pfkptr9mSZn5Fe"}
                               ]
                               },
                          media_stream_constraints={"video": True, "audio": False})
    
imgout_place = col2.empty()


while ctx.state.playing:
    with lock:
        img = img_container["img"]
    if img is None:
        continue
    # phát hiện khuôn mặt, đóng khung 
    imgout = cv2.flip(img, 0)

    imgout_place.image(imgout, channels="BGR")