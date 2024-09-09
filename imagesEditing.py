# import opencv2
import cv2
import numpy as np

def recolorImage(imagesToRecolor, newColor):
    hsv = cv2.cvtColor(imagesToRecolor, cv2.IMREAD_GRAYSCALE)
    # Define lower and upper limits of what we call "brown"
    lower = np.array([0, 0, 25])
    higher = np.array([0, 0, 255])

    hsv_img = cv2.cvtColor(imagesToRecolor, cv2.IMREAD_GRAYSCALE)  # rgb to hsv color space

    s_ch = hsv_img[:, :, 1]  # Get the saturation channel

    thesh = cv2.threshold(s_ch, 200, 3, cv2.THRESH_BINARY)[
        1]  # Apply threshold - pixels above 5 are going to be 255, other are zeros.
    thesh = cv2.morphologyEx(thesh, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (
    7, 7)))  # Apply opening morphological operation for removing artifacts.

    cv2.floodFill(thesh, None, seedPoint=(0, 0), newVal=128, loDiff=1,
                  upDiff=1)  # Fill the background in thesh with the value 128 (pixel in the foreground stays 0.

    imagesToRecolor[thesh == 128] = (0, 0, 255)  # Set all the pixels where thesh=128 to red.

    return imagesToRecolor

# Read the image
image = cv2.imread("D:\\Morgan\\phoneIconEditing\\images\\image1.jpg")

newColor = (0, 0, 255)

image = recolorImage(image, newColor)

cv2.imwrite('tulips_red_bg.jpg', image)  # Save the output image.

cv2.imshow("color changed image", image)

cv2.imwrite('output_image.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, 90])

cv2.waitKey(0)
cv2.destroyAllWindows()