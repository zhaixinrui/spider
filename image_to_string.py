import pytesseract
from PIL import Image

def image_to_string(img):
    image=Image.open(img)
    image.save('./tmp.jpg')
    image=Image.open('./tmp.jpg')
    vcode=pytesseract.image_to_string(image)
    print vcode
    return vcode


if __name__ == '__main__':
    import sys
    image_to_string(sys.argv[1])