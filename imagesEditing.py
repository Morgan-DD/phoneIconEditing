# Import the Packages
import colorsys
import os
import random
import subprocess
from colorsys import rgb_to_hsv, hsv_to_rgb
from os import mkdir
from PIL import Image
from colorthief import ColorThief
from time import gmtime, strftime, perf_counter

# margin between icon and border
margin = 15 # 15 recommended

# os used, ios or android
osName = "ios"

# if True, use the background, else use a color
useBackgroundImage = True

# folor to recolor the icons, if (0,0,0) we use the dominantColor darker or lighter
replacementIconColor = (0,0,0)

# size of icon, max is the size of the smallest icon (should be 512(px))
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

# list of id of icon folder that we want to make
wantedIcon = {}

# list of icon path
icons = {}

# list of all icon type available (folder)
allIconType = os.listdir(iconPath)

# name of all the icon type used linked by -
allIconTypeNameMerged = ""

# write all the icons type available with the number of icon for each type
idFolder = 0
for folderName in allIconType:
    idFolder+=1
    print("[" + str(idFolder) + "] " + folderName + "(" + str(len(os.listdir(iconPath + "\\" + folderName))) + " icons)")
stayOnWhile = True
while stayOnWhile:
    stayOnWhile = False
    print("\r", end='', flush=True)
    print("Icon type that you want to use , you can add multiple with space between them(number): ", end='', flush=True)
    wantedIcon = input()
    answerIsRight = True

    for wantedIconId in wantedIcon.split(" "):
        if not wantedIconId.isdigit() or wantedIconId == " " or wantedIconId == "" or int(wantedIconId) > len(allIconType):
            stayOnWhile = True

for singelWantedIcon in wantedIcon.split(" "):
    if allIconTypeNameMerged == "":
        allIconTypeNameMerged = allIconType[int(singelWantedIcon)-1]
    else:
        allIconTypeNameMerged += "-" + allIconType[int(singelWantedIcon) - 1]
    if len(icons) == 0:
        icons = list(map(lambda x: os.path.join(os.path.abspath(iconPath + "\\" + allIconType[int(singelWantedIcon)-1]), x),
                         os.listdir(iconPath + "\\" + allIconType[int(singelWantedIcon)-1])))
    else:
        icons += list(map(lambda x: os.path.join(os.path.abspath(iconPath + "\\" + allIconType[int(singelWantedIcon)-1]), x),
                         os.listdir(iconPath + "\\" + allIconType[int(singelWantedIcon)-1])))

# list of backgrounds
backgrounds = os.listdir(backgroundPath)

# background choose on the background list
wantedBackground = ""

idBackground = 0
for backgroundName in backgrounds:
    idBackground+=1
    print("[" + str(idBackground) + "] " + backgroundName.split(".")[0])
stayOnWhile = True
while stayOnWhile:
    stayOnWhile = False
    print("\r", end='', flush=True)
    print("background type that you want to use(number): ", end='', flush=True)
    wantedBackground = input()
    answerIsRight = True
    if not wantedBackground.isdigit() or wantedBackground == " " or wantedBackground == "" or int(wantedBackground) > len(backgrounds):
            stayOnWhile = True

for background in backgrounds:
    if backgrounds[int(wantedBackground)-1].lower() in background.lower():
        # background used
        BackgroundUsed = background

if BackgroundUsed == "":
    BackgroundUsed = backgrounds[0]

# opacity of pixels to put darker than the rest on the icon (border)
opacityLimitForReplacement = 100

# list of param for the generation of the icons
settings = (BackgroundType, (0, 0, 0))

# settings that will not change or get returned
staticSettings = (outPutPath, executionDate, opacityLimitForReplacement, outPutPath + "\\" + executionDate + "\\" + BackgroundUsed.split(".")[0] + "_" + allIconTypeNameMerged, replaceIconColor, replacementIconColor, iconSize)
#                  0                1             2                                                          3                                            4                5                  6
# add a background to an icon
# iconFullPath -> fullPath of the icon
# backgroundFullPath -> fullPath of the background image
def addBackgroundToImage(iconFullPath, backgroundFullPath, backgroundOption, colorThemeBase, settings, staticSettings):
    """
    :param iconFullPath: full path of the icon to paste on background
    :param backgroundFullPath: full path of the background image
    :param backgroundOption: if True we use the background image, else we use a background color
    :param colorThemeBase: color theme to use on the background if image is not used
    :param settings: list of setting that are going to change and be return at the end:
    [0] -> type of background (D == dark, B == Bright, a == undefined)
    [1] -> color of modification (color that is going to replace the default icon color if staticSettings[4] is True)
    :param staticSettings: list of static settings:
    [0] -> output path, where the output image are going to be put
    [1] -> date of execution
    [2] -> opacity of pixels to be darker than the rest on the icon (border)
    [3] -> full path of the folder on the date of the execution folder on the output folder
    [4] -> if True, replace the color of the icon (base black)
    [5] -> color to recolor the icons, if (0,0,0) we use the colorThemeBase darker or lighter
    [6] -> size of the icon (going to be resized)
    :return:
    """
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
    # if we want to change the color of the icon and there is no new color define
    if staticSettings[4] and staticSettings[5][0] == 0 and staticSettings[5][1] == 0 and staticSettings[5][2] == 0:
        # get the HSV code of the colorThemeBase(dominant color on background)
        hTheme, sTheme, vTheme = colorsys.rgb_to_hsv(colorThemeBase[0], colorThemeBase[1], colorThemeBase[2])
        # if the type of background is undefined
        if BackgroundType == "a":
            # if the background is dark
            if vTheme > 127:
                # we set the color to be lighter than the background
                ModificationColor = tuple(map(int, hsv_to_rgb(hTheme, sTheme, vTheme - ModifyColorScale)))
                ModificationColor2 = tuple(map(int, hsv_to_rgb(hTheme, sTheme, vTheme - ModifyColorScale*2)))
            # if the background is light
            else:
                # we set the color to be darker if than the lighter
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
    if staticSettings[4] and staticSettings[5][0] == 0 and staticSettings[5][1] == 0 and staticSettings[5][2] == 0:
        # get the alpha of the icon
        alphaData = front.split()[-1]
        # check all pixels
        for x in range(front.size[0]):
            for y in range(front.size[1]):
                # get the precise pixel
                pixelColor = alphaData.getpixel((x, y))
                front.putpixel((x, y), (ModificationColor[0], ModificationColor[1], ModificationColor[2], pixelColor))
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
    print("background color recovery...")
    dominant_colors = ()
    color_thief = ColorThief(imageToGetPaletPath)

    dominant_colors += (color_thief.get_color(quality=1))
    return dominant_colors

def folderCreation(outPutPath, executionDate, background, wantedIcon):
    if not os.path.exists(outPutPath):
        mkdir(outPutPath)
    if not os.path.exists(outPutPath + "\\" + executionDate):
        mkdir(outPutPath + "\\" + executionDate)
    if not os.path.exists(outPutPath + "\\" + executionDate + "\\" + background + "-" + wantedIcon):
        mkdir(outPutPath + "\\" + executionDate + "\\" + background + "_" + wantedIcon)


# dominant color of the background
dominantColor = getColorPalet(backgroundPath + "\\" + BackgroundUsed)

# create folder that doesn't exist
folderCreation(outPutPath, executionDate, BackgroundUsed.split(".")[0], allIconTypeNameMerged)

# number of icon to make
idIcon = 0

# check all icons
for icon in icons:
    idIcon+=1
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

subprocess.run(['explorer.exe', staticSettings[3]])