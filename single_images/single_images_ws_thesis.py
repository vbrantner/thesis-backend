import asyncio
import time

import cv2
import websockets

# Kamera ini 
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
camera.set(cv2.CAP_PROP_FPS, 10)


async def video_stream(websocket, path):
    while True:
        start_time = time.time()  # Startzeit für die Zeitmessung
        success, frame = camera.read()  # Bild von der Kamera lesen
        if not success:
            print("Failed to grab frame")
            break
        ret, buffer = cv2.imencode(".jpg", frame)  # Das Bild in JPEG-Format kodieren
        frame = buffer.tobytes()  # Umwandlung des kodierten Bildes in Bytes
        end_time = time.time()  # Endzeit für die Zeitmessung

        # Send the frame over the WebSocket
        try:
            await websocket.send(frame)
        except websockets.exceptions.ConnectionClosed:
            print("Connection closed")
            break


# Start the WebSocket server
start_server = websockets.serve(video_stream, "", 3000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
