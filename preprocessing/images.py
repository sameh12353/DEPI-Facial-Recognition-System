import numpy as np
import cv2

def preprocess(img):
    """
    Preprocess the image for the model.
    1. Convert from BGR to RGB.
    2. Normalize the pixel values to [0, 1].
    3. Resize the image to (224, 224).
    """
    # Check if the image is in 3-channel (RGB/BGR) format
    if len(img.shape) == 3 and img.shape[2] == 3:
        # Convert BGR to RGB because OpenCV loads images in BGR format // the model expects RGB
        image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
    else:
        raise ValueError("Image must be 3-channel (RGB/BGR).")
    
    image = (image / 255.).astype(np.float32)
    image = cv2.resize(image, dsize = (224,224))

    return image

