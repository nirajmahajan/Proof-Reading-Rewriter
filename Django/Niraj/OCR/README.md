# OCR!

This section of the project implements OCR which enables one to pass images or .pdf files, handwritten or otherwise to the project for grammar check. I have used the pytesseract library built on Google's tesseract OCR API.

There are two functions in the ocr.py script :

- ocrFromImage(img_path, mode)
  	Here img_path is the path to the input image, and mode is the method of preprocessing the image (thresh or blur)
- ocrFromPdf(pdf_path, mode)
      Here pdf_path is the path to the input pdf, and mode is the method of preprocessing each image (thresh or blur)