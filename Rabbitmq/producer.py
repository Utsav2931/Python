import pika
import time
import random
import cv2
import psycopg2

connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.queue_declare(queue='job')

messageId = 1

# while(True):
#     message = f"Sending Message Id: {messageId}"

#     channel.basic_publish(exchange='', routing_key='job', body=message)

#     print(f"sent message: {message}")
    
#     time.sleep(random.randint(1, 4))

#     messageId+=1


conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="my_db"
)

# Create a cursor object
cursor = conn.cursor()
cursor.execute("DELETE FROM image")

video_path = "C:\\Users\\HP\\Downloads\\Test.mp4"
video_capture = cv2.VideoCapture(video_path)

frame_count = 0  # Initialize frame counter

while True:
    success, frame = video_capture.read()  # Read the next frame

    if not success:  # If the video has ended or cannot be read, break the loop
        break

    frame_count += 1  # Increment the frame counter

    # Convert the frame to binary format
    frame_bytes = cv2.imencode('.jpg', frame)[1].tobytes()

    # Insert the frame into the database
    insert_query = f"INSERT INTO image (id, img) VALUES ({frame_count}, {psycopg2.Binary(frame_bytes)})"
    cursor.execute(insert_query)
    conn.commit()
    job_id = str(frame_count) 

    channel.basic_publish(exchange='', routing_key='job', body=job_id)

    print(f"sent job id: {job_id}")
    
    #time.sleep(random.randint(1, 4))

    # Optionally, you can display the frames as well
    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close any open windows
video_capture.release()
cv2.destroyAllWindows()

# Close the cursor and the connection
cursor.close()
conn.close()

connection.close()