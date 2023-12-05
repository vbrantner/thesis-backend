from flask import Flask, Response
from picamera2 import Picamera2
from picamera2.encoders import MJPEGEncoder
from picamera2.outputs import FileOutput
from threading import Condition
import io

app = Flask(__name__)


# Streaming output class
class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()

    def get_frame(self):
        with self.condition:
            self.condition.wait()
            return self.frame

def generate_video_feed():
    while True:
        frame = output.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    # Return a multipart response
    return Response(generate_video_feed(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (1280, 960)}))

picam2.set_controls({
    "ExposureTime": 10000,  # in microseconds, adjust as necessary
    "AnalogueGain": 1.2,    # adjust as necessary
    "FrameRate": 60
    # Add other controls here if needed
})

output = StreamingOutput()
picam2.start_recording(MJPEGEncoder(), FileOutput(output))


if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=8000, threaded=True)
    finally:
        picam2.stop_recording()

