import cv2
import mediapipe as mp

# USER INPUT 
REFERENCE_OBJECT_HEIGHT_CM = 30   # Example: book height in cm
REFERENCE_OBJECT_PIXEL_HEIGHT = 150 # You measure this from image
image = cv2.imread("person.jpg")

if image is None:
    print("Image not found! Run height.py first.")
    exit()
h, w, _ = image.shape
# -----------------------------
# MediaPipe Pose Setup
# -----------------------------
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True)
# Convert BGR to RGB
rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# Process image
results = pose.process(rgb_image)
if not results.pose_landmarks:
    print("No person detected")
    exit()
# Get Head Position (Eyes Avg)
left_eye = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_EYE]
right_eye = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_EYE]
head_y = int(((left_eye.y + right_eye.y) / 2) * h)
# Get Feet Position (Heels Avg)
left_heel = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HEEL]
right_heel = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HEEL]
heel_y = int(((left_heel.y + right_heel.y) / 2) * h)
# Pixel Height
pixel_height = abs(heel_y - head_y)
# Convert Pixels to CM
pixels_per_cm = REFERENCE_OBJECT_PIXEL_HEIGHT / REFERENCE_OBJECT_HEIGHT_CM
real_height_cm = pixel_height / pixels_per_cm
# Display Results
print("Pixel Height:", pixel_height)
print(f"Estimated Height: {real_height_cm:.2f} cm")
# Draw measurement line
cv2.line(image, (w//2, head_y), (w//2, heel_y), (0, 255, 0), 3)
cv2.putText(image, f"{real_height_cm:.2f} cm",
            (w//2 + 10, (head_y + heel_y)//2),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

cv2.imshow("Height Result", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
