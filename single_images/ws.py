import asyncio
import websockets
import base64
from picamera2 import Picamera2
from picamera2.encoders import MJPEGEncoder
from picamera2.outputs import FileOutput
from threading import Condition, Thread
import io

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

async def stream_video(websocket, path):
    while True:
        frame = output.get_frame()
        await websocket.send(frame)

picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (1280, 960)}))
picam2.set_controls({
#    "ExposureTime": 10000,
#    "AnalogueGain": 1.2,
    "FrameRate": 60
})

output = StreamingOutput()
picam2.start_recording(MJPEGEncoder(), FileOutput(output))

async def main():
    async with websockets.serve(stream_video, "", 8000):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    finally:
        picam2.stop_recording()

