import cv2
import numpy as np
import time
import matplotlib
import logging
import os
import io
from datetime import datetime
from exif import Image
from picamera import PiCamera
from flask import Flask, render_template, send_file, make_response

matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
speed_data = []

def get_time(image):
    return datetime.strptime(image.datetime, '%Y:%m:%d %H:%M:%S') if hasattr(image, 'datetime') else None

def get_time_diff(img1, img2):
    return (get_time(img2) - get_time(img1)).total_seconds() if get_time(img1) and get_time(img2) else 0

def match_features(desc1, desc2):
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
    matches = matcher.knnMatch(desc1, desc2, k=2)
    return sorted([m for m, n in matches if m.distance < 0.6 * n.distance], key=lambda x: x.distance)

def calculate_velocity(pixel_dist, gsd, time_diff):
    return (pixel_dist * gsd) / 1000 / time_diff if time_diff > 0 else 0

cam = PiCamera()
cam.resolution = (640, 480)
cam.start_preview()
GSD = 280  
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILENAMES = [os.path.join(BASE_DIR, 'frame_a.jpg'), os.path.join(BASE_DIR, 'frame_b.jpg')]
current_idx = 0

time.sleep(1)

@app.route('/')
def main_page():
    return render_template('main.html')

@app.route('/iss_speed')
def iss_speed():
    global current_idx
    current_idx = 1 - current_idx
    time.sleep(1)
    cam.capture(FILENAMES[current_idx])
    prev_img, curr_img = Image(FILENAMES[1 - current_idx]), Image(FILENAMES[current_idx])
    dt = get_time_diff(prev_img, curr_img)
    prev_cv, curr_cv = cv2.imread(FILENAMES[1 - current_idx]), cv2.imread(FILENAMES[current_idx])
    orb = cv2.ORB_create(nfeatures=5000)
    kp1, desc1 = orb.detectAndCompute(prev_cv, None)
    kp2, desc2 = orb.detectAndCompute(curr_cv, None)
    matches = match_features(desc1, desc2) if desc1 is not None and desc2 is not None else []
    avg_move = np.median(np.linalg.norm(np.array([kp1[m.queryIdx].pt for m in matches]) - np.array([kp2[m.trainIdx].pt for m in matches]), axis=1)) if len(matches) > 10 else 0
    speed = round(calculate_velocity(avg_move, GSD, dt), 5)
    speed_data.append((datetime.now(), speed))
    cv2.imwrite('static/frame_a.jpg', prev_cv)
    cv2.imwrite('static/frame_b.jpg', curr_cv)
    return render_template('iss_speed.html', speed=speed)

@app.route('/details')
def details():
    return render_template('details.html')

@app.route('/iss-speed-graph')
def iss_speed_graph():
    return render_template('iss_speed_graph.html', timestamp=time.time())

@app.route('/get-speed-graph')
def get_speed_graph():
    if not speed_data:
        return "No data available", 404
    times, speeds = zip(*speed_data)
    plt.figure(figsize=(10, 5))
    plt.plot(times, speeds, label="ISS Speed (km/s)", color='blue', linewidth=2)
    plt.xlabel('Time')
    plt.ylabel('Speed (km/s)')
    plt.title('ISS Speed Over Time')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    response = make_response(send_file(img, mimetype='image/png'))
    response.headers["Cache-Control"] = "no-store"
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
