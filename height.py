import cv2

# Open webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera not opening")
    exit()

print("Press C to capture image")
print("Press ESC to exit")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to read frame")
        break

    cv2.imshow("Height Measurement - Camera", frame)

    key = cv2.waitKey(1) & 0xFF

    # Press C to capture image
    if key == ord('c'):
        cv2.imwrite("person.jpg", frame)
        print("Image saved as person.jpg")
        break
    # Press ESC to exit
    elif key == 27:
        break
cap.release()
cv2.destroyAllWindows()
