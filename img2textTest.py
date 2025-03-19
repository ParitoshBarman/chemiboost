import cv2
import pytesseract


# Set Tesseract path if necessary
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_image(image_path):
    """Extract text from an image using OCR"""
    print("1")
    image = cv2.imread(image_path)
    print("2")
    cv2.imshow("image", image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    print("3")
    cv2.imshow("gray 1st", gray)
    gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    print("4")
    cv2.imshow("gray", gray)
    
    custom_config = r'--oem 3 --psm 6'
    print("5")
    text = pytesseract.image_to_string(gray, config=custom_config)
    print("6")
    print(text)
    return text


# Provide the path to the image file
# image_path = "1000121654.jpg"  # Change this to your image path
image_path = "IMG20250317115754.jpg"  # Change this to your image path

# Extract text
extracted_text = extract_text_from_image(image_path)



print("Extracted JSON saved to output.json")
