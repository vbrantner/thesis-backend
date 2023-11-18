import time
import cv2
from flask import Flask, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app, support_credentials=True)  # Erlauben von Cross-Origin Requests

camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Setzen der Bildbreite
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Setzen der Bildhöhe
camera.set(cv2.CAP_PROP_FPS, 30)  # Setzen der gewünschten Bildrate (Frames per Second)


def encode_frame():
    while True:
        start_time = time.time()  # Startzeit für die Zeitmessung
        success, frame = camera.read()  # Bild von der Kamera lesen
        if not success:
            break
        else:
            ret, buffer = cv2.imencode(
                ".jpg", frame
            )  # Das Bild in JPEG-Format kodieren
            frame = buffer.tobytes()  # Umwandlung des kodierten Bildes in Bytes
            end_time = time.time()  # Endzeit für die Zeitmessung

            print(f"Time taken for frame processing: {(end_time - start_time) * 1000:.2f} milliseconds")

            # Generieren des Antwort-Streams im multipart/x-mixed-replace Format
            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


@app.route("/video_feed")
def video_feed():
    # Streamen des Videos Frame für Frame
    return Response(
        encode_frame(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="3000", debug=True)  # Starten des Flask-Servers
