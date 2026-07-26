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
    
    # Read user's exact image - DO NOT CROP
    img = cv2.imread(input_path)
    if img is None:
        print(f"Failed to load image: {input_path}")
        sys.exit(1)
        
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply CLAHE for crisp ASCII contrast
    clahe = cv2.createCLAHE(clipLimit=3.5, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    
    # Gamma adjustment
    gamma = 1.2
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    enhanced = cv2.LUT(enhanced, table)
    
    cv2.imwrite(output_path, enhanced)
    print(f"Prepped photo (uncropped, exact user photo) saved to {output_path}")

if __name__ == "__main__":
    inp = sys.argv[1] if len(sys.argv) > 1 else "developer_lucky.png"
    prep_photo(inp)
