from PIL import Image
from pdf2image import convert_from_path 
import pytesseract
import cv2
import os

# referred from https://www.pyimagesearch.com/2017/07/10/using-tesseract-ocr-python/

# inputs a path to the image to perform ocr on, and a mode which can take values 
# 	thresh or blur
# returns a string of the image content
def ocrFromImage(im_path, mode = 'thresh'):

	# load the example image and convert it to grayscale
	image = cv2.imread(im_path)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	 
	# check to see if we should apply thresholding to preprocess the
	# image
	if mode == "thresh":
		gray = cv2.threshold(gray, 0, 255,
			cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
	 
	# make a check to see if median blurring should be done to remove
	# noise
	elif mode == "blur":
		gray = cv2.medianBlur(gray, 3)
	 
	# write the grayscale image to disk as a temporary file so we can
	# apply OCR to it
	filename = "{}.png".format(os.getpid())
	cv2.imwrite(filename, gray)

	# load the image as a PIL/Pillow image, apply OCR, and then delete
	# the temporary file
	text = pytesseract.image_to_string(Image.open(filename))
	os.remove(filename)
	return text

# inputs a path to the pdf to perform ocr on, and a mode which can take values 
# 	thresh or blur
# returns a string of the image content
def ocrFromPdf(pdf_path, mode = 'thresh'):
	pages = convert_from_path(pdf_path, 500) 

	text = ""
	counter = 1
	for page in pages:
		filename = "{}_{}.png".format(os.getpid(), str(counter))
		page.save(filename, 'JPEG')
		text += ocrFromImage(filename, mode)
		os.remove(filename)
		counter += 1
	 
	return text