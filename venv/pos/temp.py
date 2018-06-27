#coding=utf-8

import time
import requests
from PIL import Image
import pytesseract




pic = requests.get('https://pos.acewill.net/captcha')

with open('code.png', 'ab') as f:
    f.write(pic.content)
    f.close()
time.sleep(3)

img = Image.open('code.png')
img.load()
img.show()

text = pytesseract.image_to_string(img)
print text