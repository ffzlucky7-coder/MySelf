import sys
import os
import cv2
import numpy as np

def prep_photo(input_path="developer_lucky.png", output_path="data/source-prepped.png"):
    if not os.path.exists(input_path):
        if os.path.exists("developer_lucky.jpg"):
            input_path = "developer_lucky.jpg"
        else:
            print(f"Error: {input_path} does not exist.")
            sys.exit(1)
            
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    img = cv2.imread(input_path)
    if img is None:
        print(f"Failed to load image: {input_path}")
        sys.exit(1)
        
    h, w, _ = img.shape
    
    # Detect face position or crop upper body 4:3 centered around face
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray_full = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_full, scaleFactor=1.1, minNeighbors=5)
    
    if len(faces) > 0:
        # Pick largest face
        fx, fy, fw, fh = max(faces, key=lambda f: f[2] * f[3])
        cy = fy + fh // 2
        cx = fx + fw // 2
    else:
        cy = int(h * 0.38)
        cx = w // 2
        
    # Crop 4:3 ratio centered
    crop_h = int(min(h, w * 3 / 4))
    crop_w = int(crop_h * 4 / 3)
    
    y1 = max(0, cy - int(crop_h * 0.4))
    y2 = min(h, y1 + crop_h)
    if y2 - y1 < crop_h:
        y1 = max(0, y2 - crop_h)
        
    x1 = max(0, cx - crop_w // 2)
    x2 = min(w, x1 + crop_w)
    if x2 - x1 < crop_w:
        x1 = max(0, x2 - crop_w)
        
    cropped = img[y1:y2, x1:x2]
    
    # Save high-res compressed profile picture for user (under 1MB)
    output_profile = "lucky_profile_picture.jpg"
    cv2.imwrite(output_profile, cv2.resize(cropped, (1200, 900)), [int(cv2.IMWRITE_JPEG_QUALITY), 92])
    print(f"Compressed 4:3 profile picture saved to {output_profile} ({os.path.getsize(output_profile)/1024:.1f} KB)")
    
    # Convert to grayscale for ASCII prep
    gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
    
    # Apply CLAHE for strong ASCII highlights
    clahe = cv2.createCLAHE(clipLimit=4.5, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    
    gamma = 1.3
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    enhanced = cv2.LUT(enhanced, table)
    
    cv2.imwrite(output_path, enhanced)
    print(f"Prepped photo saved to {output_path}")

if __name__ == "__main__":
    inp = sys.argv[1] if len(sys.argv) > 1 else "developer_lucky.png"
    prep_photo(inp)
