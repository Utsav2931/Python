import cv2
video_path = "C:\\Users\\HP\\Downloads\\Test.mp4"  
video_capture = cv2.VideoCapture(video_path)


frame_count = 0  # Initialize frame counter

while True:
    success, frame = video_capture.read()  # Read the next frame

    if not success:  # If the video has ended or cannot be read, break the loop
        break

    frame_count += 1  # Increment the frame counter

    frame_path = f"./imgs/frame_{frame_count}.jpg"  # Path to save the frame
    cv2.imwrite(frame_path, frame)  # Save the frame as an image
    
    # Optionally, you can display the frames as well
    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close any open windows
video_capture.release()
cv2.destroyAllWindows()

