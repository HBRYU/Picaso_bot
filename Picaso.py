# 2019_7_31
# Picaso V1.1 Work in progress.
# - Install OpenCV, pynput, and pillow (pip install opencv-python pynput pillow).
# - Do not touch or move the mouse while running.
# - To terminate, press ESC.

# 2021_12_26
# just way fucking better in every possible aspect

import cv2
import os
import time
import numpy as np
from PIL import ImageGrab, Image

from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController

from pynput.keyboard import Listener

keyboard = KeyboardController()
mouse = MouseController()

mouse = MouseController()
keyboard = KeyboardController()

#I'm gonna butcher this code a bit hopefully it doesn't shit itself catastrophically

# Start ms paint maximized using cmd commands.
#os.system("Start /max mspaint")
# Wait for ms paint to actually start before spamming left click.
#time.sleep(1)
# Drawing top left starting point pixel coordinates.
# Tweak this based on monitor resolution
START_POS = (200, 200)
# Set mouse position.
#mouse.position = START_POS


def on_press(key):
    # print("{} pressed".format(key))
    if key == Key.esc:
        os._exit(1)


def find_edit_button():
    edit_colors_button = cv2.imread("templates/edit_colors_button.png")
    h, w, c = edit_colors_button.shape

    # Grab an image of the application.
    img = ImageGrab.grab(bbox=None)
    img = np.array(img)
    # Convert to standard RGB.
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Match to template edit button image.
    res = cv2.matchTemplate(img, edit_colors_button, cv2.TM_SQDIFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = min_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    # Calculate coordinates of button center.
    center = ((top_left[0] + bottom_right[0]) / 2, (top_left[1] + bottom_right[1]) / 2)
    return center


def find_fields():
    field = cv2.imread("templates/color_field 2.png")
    ok_button = cv2.imread("templates/ok_button.png")
    h, w, c = field.shape

    #I am very smart.###########
    x_offset = 50
    ############################

    # Grab an image of the application.
    img = ImageGrab.grab(bbox=None)
    img = np.array(img)
    # Convert to standard RGB.
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Match to template field image.
    res = cv2.matchTemplate(img, field, cv2.TM_SQDIFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = min_loc
    bottom_right = (top_left[0] + w + x_offset, top_left[1] + h)

    # Calculate coordinates of fields, assuming constant distance between boxes.
    red = ((top_left[0] + bottom_right[0]) / 2, (top_left[1] + bottom_right[1]) / 2)
    blue = (red[0], red[1] + 35)
    green = (red[0], red[1] + 60)

    # Match to template OK button.
    res = cv2.matchTemplate(img, ok_button, cv2.TM_SQDIFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = min_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    button = ((top_left[0] + bottom_right[0]) / 2, (top_left[1] + bottom_right[1]) / 2)

    ret = {
        "red": red,
        "blue": blue,
        "green": green,
        "ok": button
    }
    # cv2.rectangle(img, top_left, bottom_right, 255, 2)
    return ret


def clear_field():
    for i in range(3):
        time.sleep(0.05)
        keyboard.press(Key.backspace)
        time.sleep(0.05)
        keyboard.press(Key.delete)


def update_RGB(grayThresh):
    # SELECT COLOR Button pixel coordinates
    mouse.position = find_edit_button()
    mouse.click(Button.left, 1)
    time.sleep(3)
    fields = find_fields()

    # SELECT COLOR\RED Button pixel coordinates
    mouse.position = fields["red"]
    mouse.click(Button.left, 1)
    clear_field()
    # Enter the max rgb value (grayThresh) in COLOR\RED
    keyboard.type(str(grayThresh))

    # SELECT COLOR\BLUE Button pixel coordinates
    mouse.position = fields["blue"]
    mouse.click(Button.left, 1)
    clear_field()
    # Enter the max rgb value (grayThresh) in COLOR\BLUE
    keyboard.type(str(grayThresh))

    # SELECT COLOR\GREEN Button pixel coordinates
    mouse.position = fields["green"]
    mouse.click(Button.left, 1)
    clear_field()
    # Enter the max rgb value (grayThresh) in COLOR\GREEN
    keyboard.type(str(grayThresh))

    time.sleep(0.1)
    # OK Button pixel coordinates
    mouse.position = fields["ok"]
    # Clicks it, returns to canvas
    mouse.click(Button.left, 1)
    # Reseting mouse position to starting position
    mouse.position = START_POS
    time.sleep(0.1)

'''
#-----------2021 10 29 FUCK
def grayscale(imgPath):
    img = Image.open(imgPath).convert('L')
    img.save("temp_grayscale.png")
'''

def draw_image(imgPath, step):
    img = cv2.imread(imgPath)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # Gray brightness value AKA current max rgb value
    grayThresh = 0
    # Gray brightness value increase amount
    # Tweak for speed
    threshStep = step

    while grayThresh < 255:
        # Prints the current max rgb value
        print("GrayThresh :", grayThresh)
        # Prints the percentage (%)
        print(str(int((grayThresh / 255) * 100)) + "%")

        # Skip values that aren't present in the image
        if grayThresh in img:
            print("GrayThresh: " + str(grayThresh))
            update_RGB(grayThresh)
        else:
            grayThresh += threshStep
            continue

        '''I'm about to fuck this up, so here's a backup:
        
        for i in range(len(img)):
            mouse.position = (START_POS[0], mouse.position[1])
            mouse.move(0, 1)
            for j in range(len(img[i])):
                mouse.position = (START_POS[0] + j, START_POS[1] + i)
                if grayThresh - threshStep < img[i, j, 0] and img[i, j, 0] <= grayThresh:
                    # Click (paint)
                    mouse.click(Button.left, 1)
                    # Speed, faster more errors
                    time.sleep(0.001)
        grayThresh += threshStep
        '''
        
        for i in range(len(img)):
            mouse.position = (START_POS[0], START_POS[1]+i)
            #mouse.move(0, 1)
            for j in range(len(img[i])):
                if grayThresh - threshStep < img[i, j, 0] and img[i, j, 0] <= grayThresh:
                    mouse.position = (START_POS[0] + j, START_POS[1] + i)
                    mouse.press(Button.left)
                    if j < len(img[0])-1 and grayThresh - threshStep < img[i, j+1, 0] and img[i, j+1, 0] <= grayThresh:
                        continue
                    else:
                        mouse.release(Button.left)
                    # Click (paint)
                    #mouse.click(Button.left, 1)
                    # Speed, faster more errors
                    time.sleep(0.001)
        grayThresh += threshStep   

def UI():
    print("Picaso Bot V.2021.10.30\nby HBRYU")
    image_name = input("Enter image file name (including file extension, must be located within the Images/ directory): ")
    imgPath = "Images/" + image_name
    threshStep = int(input("Enter greyscale threshold step (high: faster, less detail, must be an integer): "))
    print("You can press the ESC key to exit the drawing sequence")
    print("Starting in \n3,")
    time.sleep(1)
    print("2,")
    time.sleep(1)
    print("1, ")
    time.sleep(1)
    
    #starting sequence
    os.system("Start /max mspaint")
    mouse.position = START_POS
    time.sleep(1)
    
    # Keyboard termination, ESC
    listener = Listener(on_press=on_press)
    listener.start()
    #grayscale("Images/whatthefuck.png")
    draw_image(imgPath, threshStep)
    
UI()

