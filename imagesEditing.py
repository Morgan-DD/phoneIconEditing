# Import the Packages
import colorsys
import os
import random
import subprocess
from colorsys import rgb_to_hsv, hsv_to_rgb
from os import mkdir
from PIL import Image
from colorthief import ColorThief
from time import gmtime, strftime

# margin between icon and border
margin = 15 # 15 recommended

# color to recolor the icons
replacementIconColor = (0,0,0)

# size of icon
iconSize = 100

# if True, replace the color of the icon (base black)
replaceIconColor = True

# True if the background is mostly dark
BackgroundType = "a"

# name of the background wanted
wantedBackgroundName = "venom"

# background used
BackgroundUsed = ""

# folder where the script is executed (and where pics are)
executionFolder = os.path.dirname(os.path.realpath(__file__))

# date of execution of the script
executionDate = strftime("%Y-%m-%d_%H-%M", gmtime())

# path of icons and backgrounds folder
iconPath = executionFolder + "\\images\\icon"
backgroundPath = executionFolder + "\\images\\background"

# path of output folder
outPutPath = executionFolder + "\\output"

# get the icons and backgrounds path on the folders define (iconPath and backgroundPath)
icons = os.listdir(iconPath)
backgrounds = os.listdir(backgroundPath)

for background in backgrounds:
    if wantedBackgroundName.lower() in background.lower():
        # background used
        BackgroundUsed = background

if BackgroundUsed == "":
    BackgroundUsed = backgrounds[0]

# opacity of pixels to put black
opacityLimitForReplacement = 100

# list of param for the generation of the icons
settings = (BackgroundType, (0, 0, 0))

# settings that will not change or get returned
staticSettings = (outPutPath, executionDate, opacityLimitForReplacement, outPutPath + "\\" + executionDate + "\\" + BackgroundUsed.split(".")[0], replaceIconColor, replacementIconColor, iconSize)
#                  0                1             2                                                          3                                            4                5                  6
# add a background to an icon
# iconFullPath -> fullPath of the icon
# backgroundFullPath -> fullPath of the background image
def addBackgroundToImage(iconFullPath, backgroundFullPath, options, colorThemeBase, settings, staticSettings):
    # get the front icon
    front = Image.open(iconFullPath)
    front = front.convert("RGBA")
    # type of background (D == dark, B == Bright, a == undefined)
    BackgroundType = settings[0]
    # color of modification
    ModificationColor = settings[1]
    # more changed color
    ModificationColor2 = (0,0,0)
    # modify color scale
    ModifyColorScale = 50
    # get the
    if staticSettings[4] and staticSettings[5][0] == 0 and staticSettings[5][1] == 0 and staticSettings[5][2] == 0:
        hTheme, sTheme, vTheme = colorsys.rgb_to_hsv(colorThemeBase[0], colorThemeBase[1], colorThemeBase[2])
        if BackgroundType == "a":
            if vTheme > 127:
                ModificationColor = tuple(map(int, hsv_to_rgb(hTheme, sTheme, vTheme - ModifyColorScale)))
                ModificationColor2 = tuple(map(int, hsv_to_rgb(hTheme, sTheme, vTheme - ModifyColorScale*2)))
            else:
                ModificationColor = tuple(map(int, hsv_to_rgb(hTheme, sTheme, vTheme + ModifyColorScale)))
                ModificationColor2 = tuple(map(int, hsv_to_rgb(hTheme, sTheme, vTheme + ModifyColorScale * 2)))

        for i in range(len(ModificationColor)):
            if ModificationColor[i] > 255:
                ModificationColor[i] = 254
            if ModificationColor2[i] > 255:
                ModificationColor2[i] = 254
            if ModificationColor[i] < 0:
                ModificationColor[i] = 0
            if ModificationColor2[i] < 0:
                ModificationColor2[i] = 0

    # if we want to modify the color of the icons, and we don't have defined a new color
    if staticSettings[4] and staticSettings[5][0] == 0 and staticSettings[5][1] == 0 and staticSettings[5][2] == 0:
        alphaData = front.split()[-1]
        for x in range(front.size[0]):
            for y in range(front.size[1]):
                pixelColor = alphaData.getpixel((x, y))
                if pixelColor > 0:
                    if pixelColor < staticSettings[2]:
                        front.putpixel((x, y), ModificationColor2)
                    else:
                        front.putpixel((x, y), ModificationColor)
    elif staticSettings[4] and (staticSettings[5][0] > 0 or staticSettings[5][1] > 0 or staticSettings[5][2] > 0):
        alphaData = front.split()[-1]
        for x in range(front.size[0]):
            for y in range(front.size[1]):
                pixelColor = alphaData.getpixel((x, y))
                if pixelColor > 0:
                    front.putpixel((x, y), staticSettings[5])

    # resize the background to fit the size of the icon
    front.thumbnail((staticSettings[6],staticSettings[6]), Image.Resampling.LANCZOS)

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

    # Pasting icon image on top of background
    back.paste(front, (margin, margin), mask=front)

    # Displaying the image
    # back.show()
    back.save(staticSettings[3] + "\\" + iconFullPath.split("\\")[-1])

    return BackgroundType, ModificationColor



def complementary(r, g, b):
    """returns RGB components of complementary color"""
    hsv = rgb_to_hsv(r, g, b)
    return hsv_to_rgb((hsv[0] + 0.5) % 1, hsv[1], hsv[2])


def getColorPalet(imageToGetPaletPath):
    dominant_colors = ()
    color_thief = ColorThief(imageToGetPaletPath)

    dominant_colors += (color_thief.get_color(quality=1))
    return dominant_colors

def folderCreation(outPutPath, executionDate, background):
    if not os.path.exists(outPutPath):
        mkdir(outPutPath)
    if not os.path.exists(outPutPath + "\\" + executionDate):
        mkdir(outPutPath + "\\" + executionDate)
    if not os.path.exists(outPutPath + "\\" + executionDate + "\\" + background):
        mkdir(outPutPath + "\\" + executionDate + "\\" + background)


# dominant color of the background
dominantColor = getColorPalet(backgroundPath + "\\" + BackgroundUsed)

# create folder that doesn't exist
folderCreation(outPutPath, executionDate, BackgroundUsed.split(".")[0])

# check all icons
for icon in icons:
    # generate background for all icons
    settings = addBackgroundToImage(iconPath + "\\" + icon, backgroundPath + "\\" + BackgroundUsed, "B,R",
                                    dominantColor, settings, staticSettings)
# print(dominantColor)
# print(settings[1])

newColorIMage = Image.new(mode="RGB", size=(500, 500),
                          color=settings[1])
dominantColorImage = Image.new(mode="RGB", size=(500, 500),
                               color=dominantColor)

subprocess.run(['explorer.exe', staticSettings[3]])

# Image.open(dominantColor).show()

# dominantColorImage.show(title="dominantColorImage")
# newColorIMage.show(title="newColorIMage")

# print(complementary(160, 32, 240))
# cv2.waitKey(0)
# cv2.destroyAllWindows()
