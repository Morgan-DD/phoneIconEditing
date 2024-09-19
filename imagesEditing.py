# Import the Packages
import colorsys
import os
import random
import subprocess
from colorsys import rgb_to_hsv, hsv_to_rgb
from os import mkdir
from PIL import Image
from colorthief import ColorThief
from time import localtime, strftime
import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys

# margin between icon and border
margin = 15  # 15 recommended

# os used, ios or android
osName = "ios"

# if True, use the background, else use a color
useBackgroundImage = True

# color to recolor the icons, if (0,0,0) we use the dominantColor darker or lighter
replacementIconColor = (0, 0, 0)

# size of icon, max is the size of the smallest icon (should be 512(px))
iconSize = 100

# if True, replace the color of the icon (base black)
replaceIconColor = True

# if True, we add border to the icon
addBorderToIcon = False

# True if the background is mostly dark
BackgroundType = "a"

# name of the background wanted
wantedBackgroundName = "venom"

# background used
BackgroundUsed = ""

# folder where the script is executed (and where pics are)
executionFolder = os.path.dirname(os.path.realpath(__file__))

# date of execution of the script
executionDate = strftime("%Y-%m-%d_%H-%M", localtime())

# path of icons and backgrounds folder
iconPath = executionFolder + "\\images\\icon"
backgroundPath = executionFolder + "\\images\\background"

# path of output folder
outPutPath = executionFolder + "\\output"

# list of id of icon folder that we want to make
wantedIcon = {}

# list of icon path
icons = {}

# list of all icon type available (folder)
allIconType = os.listdir(iconPath)

# name of all the icon type used linked by -
allIconTypeNameMerged = ""

# if there is more than 1 icon type available
if len(allIconType) > 1:
    # write all the icons type available with the number of icon for each type
    idFolder = 0
    for folderName in allIconType:
        idFolder += 1
        # write the name of the folder and the number of icons in that folder
        print("[" + str(idFolder) + "] " + folderName + "(" + str(
            len(os.listdir(iconPath + "\\" + folderName))) + " icons)")
    # variable used for the loop
    stayOnWhile = True
    while stayOnWhile:
        # set value to exit the while
        stayOnWhile = False
        # print a line for asking the user an answer
        print("\r", end='', flush=True)
        print("Icon type that you want to use, you can add multiple with space between them(number): ", end='',
              flush=True)
        wantedIcon = input()
        answerIsRight = True
        # foreach the answers (split by space " ")
        for wantedIconId in wantedIcon.split(" "):
            # if the answer is not and number or a bigger number than the length of the icon folder list
            if not wantedIconId.isdigit() or wantedIconId == " " or wantedIconId == "" or int(wantedIconId) > len(
                    allIconType):
                # we stay on the while
                stayOnWhile = True

    #  |--| this part is used to generate the name of output folder name with the type of icons used |--|
    #  foreach the answers (split by space " ")
    for singleWantedIcon in wantedIcon.split(" "):
        # if the name is empty
        if allIconTypeNameMerged == "":
            # we add the name of the first icon type to the name
            allIconTypeNameMerged = allIconType[int(singleWantedIcon) - 1]
        # if the name is already started
        else:
            # we add "-" and the name of the icon type
            allIconTypeNameMerged += "-" + allIconType[int(singleWantedIcon) - 1]
        # if the list of icon type used is empty
        if len(icons) == 0:
            # we define the list with the value of this icon type
            icons = list(
                map(lambda x: os.path.join(os.path.abspath(iconPath + "\\" + allIconType[int(singleWantedIcon) - 1]),
                                           x),
                    os.listdir(iconPath + "\\" + allIconType[int(singleWantedIcon) - 1])))
        # if the list of icon type used is NOT empty
        else:
            # we add the values for this icon type
            icons += list(
                map(lambda x: os.path.join(os.path.abspath(iconPath + "\\" + allIconType[int(singleWantedIcon) - 1]),
                                           x),
                    os.listdir(iconPath + "\\" + allIconType[int(singleWantedIcon) - 1])))
# if there is only 1 icon type available
else:
    # we define the list with the value of the only icon type
    icons = list(
        map(lambda x: os.path.join(os.path.abspath(iconPath + "\\" + allIconType[int(0) - 1]), x),
            os.listdir(iconPath + "\\" + allIconType[0])))
# list of backgrounds
backgrounds = os.listdir(backgroundPath)

# background choose on the background list
wantedBackground = ""
# if there is more than 1 background
if len(backgrounds) > 1:
    # write all the background available (name of the file without extension)
    idBackground = 0
    # foreach on all the backgrounds
    for backgroundName in backgrounds:
        idBackground += 1
        # display the background's name
        print("[" + str(idBackground) + "] " + backgroundName.split(".")[0])
    # variable used for the loop
    stayOnWhile = True
    while stayOnWhile:
        # set value to exit the while
        stayOnWhile = False
        # print a line for asking the user an answer
        print("\r", end='', flush=True)
        print("background type that you want to use(number): ", end='', flush=True)
        wantedBackground = input()
        answerIsRight = True
        # if the answer is not a number or if the number is bigger than the length of the background list
        if not wantedBackground.isdigit() or wantedBackground == " " or wantedBackground == "" or int(
                wantedBackground) > len(backgrounds):
            stayOnWhile = True
    # set the background used to the one that the user chose
    BackgroundUsed = backgrounds[int(wantedBackground) - 1].lower()
# if there is only 1 background
else:
    # we set this background
    BackgroundUsed = backgrounds[0]

# opacity of pixels to put darker than the rest on the icon (border)
opacityLimitForReplacement = 100

# list of param for the generation of the icons
settings = (BackgroundType, (0, 0, 0))

# add a background to an icon
# iconFullPath -> fullPath of the icon
# backgroundFullPath -> fullPath of the background image
def addBackgroundToImage(iconFullPath, backgroundFullPath, backgroundOption, colorThemeBase, _settings,
                         _staticSettings):
    """
    :param iconFullPath: full path of the icon to paste on background
    :param backgroundFullPath: full path of the background image
    :param backgroundOption: if True we use the background image, else we use a background color
    :param colorThemeBase: color theme to use on the background if image is not used
    :param _settings: list of setting that are going to change and be return at the end:
    [0] -> type of background (D == dark, B == Bright, a == undefined)
    [1] -> color of modification (color that is going to replace the default icon color if _staticSettings[4] is True)
    :param _staticSettings: list of static settings:
    [0] -> output path, where the output image are going to be put
    [1] -> date of execution
    [2] -> opacity of pixels to be darker than the rest on the icon (border)
    [3] -> full path of the folder on the date of the execution folder on the output folder
    [4] -> if True, replace the color of the icon (base black)
    [5] -> color to recolor the icons, if (0,0,0) we use the colorThemeBase darker or lighter
    [6] -> size of the icon (going to be resized)
    [7] -> boolean to know if we have to add border to the icon
    :return:
    """
    # thickness of the borders (px)
    BordersThickness = 2
    # get the front icon
    front = Image.open(iconFullPath)
    front = front.convert("RGBA")
    border = Image.new("RGBA", (_staticSettings[6] + margin * 2, _staticSettings[6] + margin * 2),
                       (0, 0, 0, 0))
    # type of background (D == dark, B == Bright, a == undefined)
    _backgroundType = _settings[0]
    # color of modification
    ModificationColor = _settings[1]
    # more changed color
    ModificationColor2 = (0, 0, 0)
    # modify color scale
    ModifyColorScale = 50
    # if we want to change the color of the icon and there is no new color define
    if _staticSettings[4] and _staticSettings[5][0] == 0 and _staticSettings[5][1] == 0 and _staticSettings[5][2] == 0:
        # get the HSV code of the colorThemeBase(dominant color on background)
        hTheme, sTheme, vTheme = colorsys.rgb_to_hsv(colorThemeBase[0], colorThemeBase[1], colorThemeBase[2])
        # if the type of background is undefined
        if _backgroundType == "a":
            # if the background is dark
            if vTheme > 127:
                # we set the color to be lighter than the background
                ModificationColor = tuple(map(int, hsv_to_rgb(hTheme, sTheme, vTheme - ModifyColorScale)))
                ModificationColor2 = tuple(map(int, hsv_to_rgb(hTheme, sTheme, vTheme - ModifyColorScale * 2)))
            # if the background is light
            else:
                # we set the color to be darker if than the background
                ModificationColor = tuple(map(int, hsv_to_rgb(hTheme, sTheme, vTheme + ModifyColorScale)))
                ModificationColor2 = tuple(map(int, hsv_to_rgb(hTheme, sTheme, vTheme + ModifyColorScale * 2)))
        # check for the replacement color to be a rgb code (>= 0 and <= 255)
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
    if _staticSettings[4] and _staticSettings[5][0] == 0 and _staticSettings[5][1] == 0 and _staticSettings[5][2] == 0:
        # get the alpha of the icon
        alphaData = front.split()[-1]
        # check all pixels
        for x in range(front.size[0]):
            for y in range(front.size[1]):
                # get the precise pixel
                pixelColor = int(alphaData.getpixel((x, y)))

                if pixelColor > 0:
                    front.putpixel((x, y), (
                        ModificationColor[0], ModificationColor[1], ModificationColor[2], 255))  # pixelColor
                    """
                    try:
                        if (alphaData.getpixel((x - 1, y)) == 0 or x - 1 < 0) and alphaData.getpixel((x, y)) > 0:
                            for i1 in range(BordersThickness):
                                border.putpixel((x - i1 + margin, y + margin),
                                                (0, 255, 0, 255))  # (255,0,0,pixelColor))
                    except Exception:
                        pass
                    try:
                        if (alphaData.getpixel((x + 1, y)) == 0 or x + 1 > front.size[0]) and alphaData.getpixel(
                                (x, y)) > 0:
                            for i2 in range(BordersThickness):
                                border.putpixel((x + i2 + margin, y + margin),
                                                (0, 255, 0, 255))  # (255,0,0,pixelColor))
                    except Exception:
                        pass
                    try:
                        if (alphaData.getpixel((x, y - 1)) == 0 or y - 1 < 0) and alphaData.getpixel((x, y)) > 0:
                            for i3 in range(BordersThickness):
                                border.putpixel((x + margin, y - i3 + margin),
                                                (0, 255, 0, 255))  # (255,0,0,pixelColor))
                    except Exception:
                        pass
                    try:
                        if (alphaData.getpixel((x, y + 1)) == 0 or y + 1) and alphaData.getpixel((x, y)) > 0:
                            for i4 in range(BordersThickness):
                                border.putpixel((x + margin, y + i4 + margin),
                                                (0, 255, 0, 255))  # (255,0,0,pixelColor))
                    except Exception:
                        pass
                    """
    elif _staticSettings[4] and (_staticSettings[5][0] > 0 or _staticSettings[5][1] > 0 or _staticSettings[5][2] > 0):
        alphaData = front.split()[-1]
        for x in range(front.size[0]):
            for y in range(front.size[1]):
                pixelColor = alphaData.getpixel((x, y))
                if pixelColor > 0:
                    front.putpixel((x, y), _staticSettings[5])

    # resize the background to fit the size of the icon
    front.thumbnail((_staticSettings[6], _staticSettings[6]), Image.Resampling.LANCZOS)
    border.thumbnail((_staticSettings[6], _staticSettings[6]), Image.Resampling.LANCZOS)

    if _staticSettings[7]:
        open_cv_image = np.array(front)
        # Convert RGB to BGR
        open_cv_image = open_cv_image[:, :, ::-1].copy()
        # Grayscale
        gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)

        # Find Canny edges
        edged = cv2.Canny(gray, 30, 200)
        cv2.waitKey(0)

        # Finding Contours
        # Use a copy of the image e.g. edged.copy()
        # since findContours alters the image
        contours, hierarchy = cv2.findContours(edged,
                                               cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        cv2.imshow('Canny Edges After Contouring', edged)
        cv2.waitKey(0)

        print("Number of Contours found = " + str(len(contours)))

        # Draw all contours
        # -1 signifies drawing all contours
        cv2.drawContours(image, contours, -1, (0, 255, 0), 3)

        cv2.imshow('Contours', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        """
        open_cv_image = np.array(front)

        gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)

        # binarize image
        retval, bw = cv2.threshold(gray, 0, 1, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        # find contour
        # imgEdge, contours, hierarchy = cv2.findContours(bw, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        print(cv2.findContours(bw, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE))

        plt.imshow(bw)
        plt.show()
        """
        # print(len(contours))

    # if we use the background
    if backgroundOption:
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

    # Pasting border of icon image on top of background
    back.paste(border, (margin, margin), mask=border)
    # Pasting icon image on top of background
    back.paste(front, (margin, margin), mask=front)

    # Displaying the image
    # back.show()
    back.save(_staticSettings[3] + "\\" + iconFullPath.split("\\")[-1])

    return _backgroundType, ModificationColor


def complementary(r, g, b):
    """returns RGB components of complementary color"""
    hsv = rgb_to_hsv(r, g, b)
    return hsv_to_rgb((hsv[0] + 0.5) % 1, hsv[1], hsv[2])


def getColorPalet(imageToGetPaletPath):
    print("background color recovery...", end='')
    dominant_colors = ()
    color_thief = ColorThief(imageToGetPaletPath)

    dominant_colors += (color_thief.get_color(quality=1))
    print("done")
    return dominant_colors


def folderCreation(_outPutPath, _executionDate, background, _wantedIcon):
    finalOuputPath = _outPutPath + "\\" + _executionDate + "\\" + background + "-" + _wantedIcon
    if not os.path.exists(_outPutPath):
        mkdir(_outPutPath)
    if not os.path.exists(_outPutPath + "\\" + _executionDate):
        mkdir(_outPutPath + "\\" + _executionDate)
    if not os.path.exists(finalOuputPath):
        mkdir(finalOuputPath)
    else:
        exitWhile = True
        id = 1
        while exitWhile:
            if not os.path.exists(finalOuputPath + "-" + str(id)):
                finalOuputPath += "-" + str(id)
                mkdir(finalOuputPath)
                exitWhile = False
    print("finalOuputPath: " + str(finalOuputPath))
    return finalOuputPath



# dominant color of the background
dominantColor = getColorPalet(backgroundPath + "\\" + BackgroundUsed)

# create folder that doesn't exist
ouputFullPath = folderCreation(outPutPath, executionDate, BackgroundUsed.split(".")[0], allIconTypeNameMerged)

# settings that will not change or get returned
staticSettings = (outPutPath, executionDate, opacityLimitForReplacement, ouputFullPath, replaceIconColor, replacementIconColor, iconSize, addBorderToIcon)
#                    0               1               2                                                                  3                                                              4                  5                 6           7

# number of icon to make
idIcon = 0

# check all icons
for icon in icons:
    idIcon += 1
    # generate background for all icons
    settings = addBackgroundToImage(icon, backgroundPath + "\\" + BackgroundUsed, useBackgroundImage,
                                    dominantColor, settings, staticSettings)
    print("\r", end='', flush=True)
    print(str(idIcon) + "/" + str(len(icons)) + " icons done", end='', flush=True)

# print(dominantColor)
# print(settings[1])

newColorIMage = Image.new(mode="RGB", size=(500, 500),
                          color=settings[1])
dominantColorImage = Image.new(mode="RGB", size=(500, 500),
                               color=dominantColor)

subprocess.run(["explorer.exe", staticSettings[3]])
