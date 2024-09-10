# Import the Packages
import colorsys
import os
import random
from colorsys import rgb_to_hsv, hsv_to_rgb

from PIL import Image
from colorthief import ColorThief

# margin between icon and border
margin = 8

# True if the background is mostly dark
BackgroundType = "a"


# add a background to an icon
# iconFullPath -> fullPath of the icon
# backgroundFullPath -> fullPath of the background image
def addBackgroundToImage(iconFullPath, backgroundFullPath, options, colorThemeBase, settings):
    # get the front icon
    front = Image.open(iconFullPath)
    # type of background (D == dark, B == Bright, a == undefined)
    BackgroundType = settings[0]
    # color of modification
    ModificationColor = settings[1]
    # modify color scale
    ModifyColorScale = 30
    # if we use the background
    if options.split(',')[0].upper() == "B":
        # number of time that the background is bigger than the icon (and minimized)
        backgroundSizeToCropMulti = 10
        # get the images background and icon
        back = Image.open(backgroundFullPath)
        # if the scale is too big for the background image
        if back.size[0] - ((front.size[0]) * backgroundSizeToCropMulti) < 0 or back.size[1] - (
                (front.size[1]) * backgroundSizeToCropMulti):
            # leave when the scale is not too big for the background
            exitWhile = True
            while exitWhile:
                # decrease the scale
                backgroundSizeToCropMulti = backgroundSizeToCropMulti - 1
                # if the scale is not too big for width and height
                if (back.size[0] - ((front.size[0]) * backgroundSizeToCropMulti) > 0 and back.size[1] - (
                        (front.size[1]) * backgroundSizeToCropMulti) > 0):
                    # exit the while
                    exitWhile = False
        # generate random coordinate for cropping (x and y)
        x = random.randint(0, back.size[0] - margin - ((front.size[0]) * backgroundSizeToCropMulti))
        y = random.randint(0, back.size[1] - margin - ((front.size[1]) * backgroundSizeToCropMulti))
        # crop the background
        back = back.crop(
            (x, y, x + (margin * 2) + (front.size[0] * backgroundSizeToCropMulti),
             y + (margin * 2) + (front.size[1] * backgroundSizeToCropMulti)))
        # resize the background to fit the size of the icon
        back.thumbnail((front.size[0] + margin * 2, front.size[1] + margin * 2), Image.Resampling.LANCZOS)
    # if we use a background color
    else:
        back = Image.new(mode="RGB", size=(front.size[0] + margin * 2, front.size[1] + margin * 2),
                         color=colorThemeBase)

    hTheme, sTheme, vTheme = colorsys.rgb_to_hsv(colorThemeBase[0], colorThemeBase[1], colorThemeBase[2])
    if BackgroundType == "a":
        if vTheme > 127:
            ModificationColor = tuple(map(int, hsv_to_rgb(hTheme, sTheme, vTheme - ModifyColorScale)))
        else:
            ModificationColor = tuple(map(int, hsv_to_rgb(hTheme, sTheme, vTheme + ModifyColorScale)))

    return BackgroundType, ModificationColor

    # Pasting icon image on top of background
    # back.paste(front, (margin, margin), mask=front)

    # Displaying the image
    # back.show()


def complementary(r, g, b):
    """returns RGB components of complementary color"""
    hsv = rgb_to_hsv(r, g, b)
    return hsv_to_rgb((hsv[0] + 0.5) % 1, hsv[1], hsv[2])


def getColorPalet(imageToGetPaletPath):
    dominant_colors = ()
    color_thief = ColorThief(imageToGetPaletPath)

    dominant_colors += (color_thief.get_color(quality=1))
    return dominant_colors


colorTheme = (160, 32, 240)  # (51, 32, 67)

# folder where the script is executed (and where pics are)
imagesFolder = os.path.dirname(os.path.realpath(__file__))

# path of icons and backgrounds folder
iconPath = imagesFolder + "\\images\\icon"
backgroundPath = imagesFolder + "\\images\\background"

# get the icons and backgrounds path on the folders define (iconPath and backgroundPath)
icons = os.listdir(iconPath)
backgrounds = os.listdir(backgroundPath)

# background used
BackgroundUsed = backgrounds[2]

# dominant color of the background
dominantColor = getColorPalet(backgroundPath + "\\" + BackgroundUsed)

# list of param for the generation of the icons
settings = (BackgroundType, (0, 0, 0))

# check all iconss
for icon in icons:
    # generate background for all icons
    settings = addBackgroundToImage(iconPath + "\\" + icon, backgroundPath + "\\" + BackgroundUsed, "B,R",
                                    dominantColor, settings)
print(dominantColor)
print(settings[1])

newColorIMage = Image.new(mode="RGB", size=(500, 500),
                          color=settings[1])
dominantColorImage = Image.new(mode="RGB", size=(500, 500),
                               color=dominantColor)

# Image.open(dominantColor).show()

dominantColorImage.show(title="dominantColorImage")
newColorIMage.show(title="newColorIMage")

# print(complementary(160, 32, 240))
# cv2.waitKey(0)
# cv2.destroyAllWindows()
