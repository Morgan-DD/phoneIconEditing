from PIL import Image
import os

def addBackgroundToImage(imageFullPath, backgroundFullPath):
    # Opening the primary image (used in background)
    back = backgroundFullPath.open(r"BACKGROUND_IMAGE_PATH")

    # Opening the secondary image (overlay image)
    front = imageFullPath.open(r"OVERLAY_IMAGE_PATH")

    # Pasting img2 image on top of img1
    # starting at coordinates (0, 0)
    back.paste(front, (0, 0), mask=front)

    # Displaying the image
    back.show()
    print(imageFullPath)

imagesFolder = os.path.dirname(os.path.realpath(__file__))

iconPath = imagesFolder + "\\images\\icon"
backgroundPath = imagesFolder + "\\images\\background"

icons = os.listdir(iconPath)
backgrounds = os.listdir(backgroundPath)

print(icons)

for icon in icons:
    addBackgroundToImage(iconPath + "\\" + icon, backgroundPath + "\\" + backgrounds[0])

# cv2.waitKey(0)
# cv2.destroyAllWindows()