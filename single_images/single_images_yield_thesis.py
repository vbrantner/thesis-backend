...
camera = cv2.VideoCapture(0)
 # Setzen der Bildbreite
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640) 
# Setzen der Bildhöhe
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  
 # Setzen der gewünschten Bildrate (Frames per Second)
camera.set(cv2.CAP_PROP_FPS, 30) 


def encode_frame():
    while True:
        # Bild von der Kamera lesen
        success, frame = camera.read()  
        if not success:
            break
        else:
            # Das Bild in JPEG-Format kodieren
            ret, buffer = cv2.imencode(".jpg", frame)
            # Umwandlung des kodierten Bildes in Bytes
            frame = buffer.tobytes()

            # Endzeit für die Zeitmessung
            end_time = time.time()

            # Generieren des Antwort-Streams im multipart/x-mixed-replace Format
            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


@app.route("/video_feed")
def video_feed():
    # Streamen des Videos Frame für Frame und Trennung durch bonundary
    return Response(
        encode_frame(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )
