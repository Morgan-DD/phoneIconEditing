from PIL import Image, ImageEnhance, ImageColor
import numpy as np
from array import *

image = Image.open("D:\\Morgan\\phoneIconEditing\\images\\image1.jpg")
image = image.convert("RGB")
d = image.getdata()
newImage = Image.new('RGB', (image.width,image.height))
#image.show()

newRGBColor = (255, 0, 0)
RGBForNotBackgroud = [0, 0, 0]
maximum = 0
mostFrequentColor = None
for number, color in image.getcolors():
    if number > maximum:
        maximum = number
        mostFrequentColor = color
print(mostFrequentColor)
mostFrequentColorArray = array('i', mostFrequentColor)
colorDiffrence = 100
for i in (range(0, len(mostFrequentColorArray))):
    if mostFrequentColorArray[i] > 127:
        mostFrequentColorArray[i] = mostFrequentColorArray[i] - colorDiffrence
    else:
        mostFrequentColorArray[i] = mostFrequentColorArray[i] + colorDiffrence
mostFrequentColor = tuple(mostFrequentColorArray)

for x in range(image.width):
    for y in range(image.height):
        pixel = image.getpixel((x, y))
        if pixel >= mostFrequentColor:
            newImage.putpixel((x, y), newRGBColor)
        else:
            """
            RGBForNotBackgroud[0] = newRGBColor[0] - (mostFrequentColor[0] - pixel[0])
            RGBForNotBackgroud[1] = newRGBColor[1] - (mostFrequentColor[1] - pixel[1])
            RGBForNotBackgroud[2] = newRGBColor[2] - (mostFrequentColor[2] - pixel[2])
            """
            RGBForNotBackgroud[0] = newRGBColor[0] - (mostFrequentColor[0] - pixel[0])
            RGBForNotBackgroud[1] = newRGBColor[1] - (mostFrequentColor[1] - pixel[1])
            RGBForNotBackgroud[2] = newRGBColor[2] - (mostFrequentColor[2] - pixel[2])
            newImage.putpixel((x, y), tuple(RGBForNotBackgroud))
        # Do something with the pixel value

# update image data
newImage.show()
newImage.save("geeks.jpg")
