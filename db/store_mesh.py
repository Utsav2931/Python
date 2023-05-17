import psycopg2
import cv2
import numpy as np
import mediapipe as mp
from psycopg2.extras import RealDictCursor
# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="my_db"
)


mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh 

# Initialize the face mesh model
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5)

cursor = conn.cursor(cursor_factory=RealDictCursor)

fetch_query = "SELECT * from image"
cursor.execute(fetch_query)

data = cursor.fetchall()
total_frames = 0
for d in data:
    image_data = d['img']
    i_id = d['id']
    #print("loop")
    with open(f".\\imgs\\temp_{i_id}.jpg",'wb') as file:
        file.write(image_data)
    total_frames += 1

for i in range(1, total_frames + 1):
    frame_path = f".\\imgs\\temp_{i}.jpg"  # Path to the frame
    frame = cv2.imread(frame_path)
    #cv2.imshow('Face Mesh', frame)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(frame_rgb)

        # Draw the face mesh on the frame
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            mp_drawing.draw_landmarks(
                image=frame,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1),
            )
        #print(type(frame))
    cv2.imshow('Face Mesh', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    frame_bytes = cv2.imencode('.jpg', frame)[1].tobytes()
    update_query = f"UPDATE image set img = {psycopg2.Binary(frame_bytes)} WHERE image.id = {i}"
    cursor.execute(update_query)

conn.commit()


face_mesh.close()
cv2.destroyAllWindows()
cursor.close()
conn.close()