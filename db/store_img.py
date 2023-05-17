import cv2
import psycopg2

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="my_db"
)

# Create a cursor object
cursor = conn.cursor()

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
