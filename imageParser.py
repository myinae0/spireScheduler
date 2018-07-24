try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\tesseract'

#parsedText = pytesseract.image_to_string(Image.open('shawn.png'))
#parsedText = pytesseract.image_to_string(Image.open('chris.png'))

def imageToText(nameOfFile) :
	parsedText = pytesseract.image_to_string(Image.open(nameOfFile), config='01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz -psm 6')
	return parsedText

def textToArray(text) :
	arrayText = text.strip().split('\n')
	return arrayText

def imageToTextToArray(nameOfFile) :
	arrayText = textToArray(imageToText(nameOfFile))
	return arrayText