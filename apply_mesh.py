import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh 

# Initialize the face mesh model
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5)
# Iterate over the frames
for frame_count in range(1, 131 + 1):
    # Read the frame
    frame_path = f"C:\\Users\\HP\\OneDrive\\Desktop\\Python\\db\\temp.jpg"  # Path to the frame
    frame = cv2.imread(frame_path)
    cv2.imshow('Face Mesh', frame)
    # Convert the frame to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with face mesh
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

    # Display or save the output frame
    print(type(frame))
    #cv2.imshow('Face Mesh', frame)
    frame_mesh_path = f'.\\mesh\\mesh_{frame_count}.jpg'
    cv2.imwrite(frame_mesh_path, frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the face mesh model and close any open windows
face_mesh.close()
cv2.destroyAllWindows()
