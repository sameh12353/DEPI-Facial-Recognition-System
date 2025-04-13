import cv2
import os

def take_photo(filename='photo.jpg'):
    # Start video capture (0 = default webcam)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Error: Could not open webcam.")
        return None

    print("📷 Press 's' to take a photo or 'q' to quit...")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to capture frame.")
            break

        # Show the frame
        cv2.imshow('Webcam', frame)

        # Wait for user to press a key
        key = cv2.waitKey(1) & 0xFF

        # If 's' is pressed, save the image
        if key == ord('s'):
            cv2.imwrite(filename, frame)
            print(f"✅ Photo saved as {filename}")
            break
        elif key == ord('q'):
            print("🚪 Exiting without saving.")
            break

    # Release camera and close window
    cap.release()
    cv2.destroyAllWindows()
    return filename

# Take photo
filename = take_photo()

# Display saved photo (optional)
if filename and os.path.exists(filename):
    img = cv2.imread(filename)
    cv2.imshow("Captured Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Delete the image after displaying
    os.remove(filename)
    print(f"🗑️ Deleted image: {filename}")
############################################################
############################################################
