import cv2
import psycopg2
from psycopg2.extras import RealDictCursor
import os

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="my_db"
)

cursor = conn.cursor(cursor_factory=RealDictCursor)

fetch_query = "SELECT * from image"
cursor.execute(fetch_query)

data = cursor.fetchall()
frame_count = 0

for d in data:
    image_data = d['img']
    i_id = d['id']
    #print(type(image_data))
    file_path = f".\\mesh\\mesh_{i_id}.jpg"
    
    with open(file_path, "wb") as file:
        file.write(image_data)
    
    frame_count += 1
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
output_file = ".\\video\\output_video.mp4"
video_writer = cv2.VideoWriter(output_file, fourcc, 30, (480, 848))
for i in range (1, frame_count + 1):
    frame_path = f".\\mesh\\mesh_{i}.jpg"  # Path to the frame
    frame = cv2.imread(frame_path)
    video_writer.write(frame)
    #cv2.imshow('Face Mesh', frame)
    #cv2.waitKey(1)
      # Specify the codec
video_writer.release()
    
        

cursor.close()

conn.close()
cv2.destroyAllWindows()
