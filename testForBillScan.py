import cv2
import pytesseract
import pandas as pd
import json

# Set Tesseract path if necessary
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_image(image_path):
    """Extract text from an image using OCR"""
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(gray, config=custom_config)
    print(text)
    return text

def parse_text_to_json(text):
    """Convert extracted text to JSON format"""
    lines = text.split("\n")
    data = []
    
    headers = ["Qty.", "Free", "Product", "HSN", "Pack", "Batch No.", "Exp. Dt.", "M.R.P.", "Rate", "Disc%", "CGST%", "SGST%", "Amount"]
    
    for line in lines:
        words = line.split()
        if len(words) >= len(headers):
            entry = dict(zip(headers, words))
            data.append(entry)
    
    return json.dumps(data, indent=4)

# Provide the path to the image file
# image_path = "1000121654.jpg"  # Change this to your image path
image_path = "IMG20250317115754.jpg"  # Change this to your image path

# Extract text
extracted_text = extract_text_from_image(image_path)

# Convert text to JSON
json_output = parse_text_to_json(extracted_text)

# Save to a JSON file
with open("output.json", "w") as json_file:
    json_file.write(json_output)

print("Extracted JSON saved to output.json")
