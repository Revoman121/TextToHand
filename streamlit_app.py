import streamlit as st
import cv2
import pytesseract
import os
from PIL import Image, ImageDraw, ImageFont

font_path = "fonts/Lucida Handwriting Italic.ttf"
font = ImageFont.truetype(font_path, size=30)


def convert_to_handwritten_text(image):
    # Save the uploaded image temporarily
    temp_image_path = "temp_image.jpg"
    with open(temp_image_path, "wb") as file:
        file.write(image.getbuffer())

    # Load the image using OpenCV
    img = cv2.imread(temp_image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to preprocess the image
    _, threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Perform OCR using Tesseract
    text = pytesseract.image_to_string(threshold)

    # Delete the temporary image file
    os.remove(temp_image_path)

    return text

def main():
    st.title("Digital to Handwritten Text Converter")

    # Upload image file
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Display the uploaded image
        st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)

        # Convert image to handwritten text on button click
        if st.button("Convert"):
            text = convert_to_handwritten_text(uploaded_file)

            # Create an image with Lucida Handwriting font and the converted text
            image = Image.new("RGB", (500, 500), color="white")
            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype("/Users/adityadeore/Desktop/lucida-handwriting/Lucida Handwriting Italic.ttf", size=30)  # Replace "path_to_lucida_handwriting_font" with the actual file path
            draw.text((10, 10), text, font=font, fill="black")

            # Display the handwritten text image
            st.image(image, caption='Handwritten Text', use_column_width=True)

if __name__ == "__main__":
    main()
