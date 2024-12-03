from flask import Flask, render_template, Response
from flask_socketio import SocketIO
import cv2
from pyngrok import ngrok

app = Flask(__name__)
socketio = SocketIO(app)

# Access laptop's default camera
camera = cv2.VideoCapture(0)

# Generate frames from the camera
def generate_frames():
    while True:
        ret, frame = camera.read()
        if not ret:
            break
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# Route to display video feed
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Route to serve the main dashboard
@app.route('/')
def index():
    return render_template('index.html')

# Expose the app online using ngrok
public_url = ngrok.connect(5000)
print(f"Public URL: {public_url}")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
