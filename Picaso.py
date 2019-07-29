#2019_7_29
#Picaso V1.0 Work in progress By u/HBRYU
# - Set ms paint to fullscreen before running this script
# - Do not touch or move the mouse while running, unless you want to shut it down.
# - ALL PIXEL COORDINATE VALUES ARE SET FOR 1920 * 1080 DISPLAY. If your moniter has a different
# 	aspect ratio, please set the coordinates to your value
# - Install OpenCV and pynput (pip install {opencv-python/pynput})

# I don't have much time to improve algorithm, such as only painting on the required pixels
# instead of scanning through the whole canvas like a printer. I'll be on it.

# Also, there is no fail safe... so if it goes wrong you just have to repeatedly spam alt+F4
# on the command prompt and prey that it to somehow shuts down. If you can *reach it.*

from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController

keyboard = KeyboardController()
mouse = MouseController()
import cv2
import numpy as np
import os
import time

mouse = MouseController()
keyboard = KeyboardController()

img = cv2.imread("!!YOUR IMAGE HERE!!") #Your image file in the same directory of this script
grayThresh = 0							#Gray brightness value
threshStep = 15							#Gray brightness value increase amount

os.system("Start mspaint")				#Image file (Grayscale)

time.sleep(1)

mouse.position  = (400, 400)			#Drawing top left starting point pixel coordinates

while grayThresh < 255:

	print("GrayThresh :", grayThresh)
	print((grayThresh / 255) * 100, "%")
	
	for i in range(len(img)):
		mouse.position = (400, mouse.position[1])
		mouse.move(0, 1)
		for j in range(len(img[i])):
			if keyboard.shift_pressed:		#FAIL SAFE <NOT WORKING!!!>
				grayThresh = 500			#End loop
		
			if grayThresh - threshStep < img[i, j, 0] <= grayThresh:
				mouse.click(Button.left, 1)
				time.sleep(0.0005)
			mouse.move(1, 0)
			#print(mouse.position)
			
				
	grayThresh += threshStep
	
	print("GrayThresh :", grayThresh)
	
	mouse.position = (1030, 80)		#SELECT COLOR Button pixel coordinates
	mouse.click(Button.left, 1)
	time.sleep(0.5)
	
	mouse.position = (1200, 600)	#SELECT COLOR\RED Button pixel coordinates
	mouse.click(Button.left, 1)
	time.sleep(0.05)
	keyboard.press(Key.backspace)
	time.sleep(0.05)
	keyboard.press(Key.backspace)
	time.sleep(0.05)
	keyboard.press(Key.backspace)
	time.sleep(0.05)
	keyboard.press(Key.delete)
	time.sleep(0.05)
	keyboard.press(Key.delete)
	time.sleep(0.05)
	keyboard.press(Key.delete)
	time.sleep(0.05)
	keyboard.type(str(grayThresh))
	
	mouse.position = (1200, 630)	#SELECT COLOR\BLUE Button pixel coordinates
	mouse.click(Button.left, 1)
	time.sleep(0.05)
	keyboard.press(Key.backspace)
	time.sleep(0.05)
	keyboard.press(Key.backspace)
	time.sleep(0.05)
	keyboard.press(Key.backspace)
	time.sleep(0.05)
	keyboard.press(Key.delete)
	time.sleep(0.05)
	keyboard.press(Key.delete)
	time.sleep(0.05)
	keyboard.press(Key.delete)
	time.sleep(0.05)
	keyboard.type(str(grayThresh))
	
	mouse.position = (1200, 660)	#SELECT COLOR\GREEN Button pixel coordinates
	mouse.click(Button.left, 1)
	time.sleep(0.05)
	keyboard.press(Key.backspace)
	time.sleep(0.05)
	keyboard.press(Key.backspace)
	time.sleep(0.05)
	keyboard.press(Key.backspace)
	time.sleep(0.05)
	keyboard.press(Key.delete)
	time.sleep(0.05)
	keyboard.press(Key.delete)
	time.sleep(0.05)
	keyboard.press(Key.delete)
	time.sleep(0.05)
	keyboard.type(str(grayThresh))
	
	time.sleep(0.1)
	mouse.position = (740, 685)		#OK Button pixel coordinates
	mouse.click(Button.left, 1)
	mouse.position = (400, 400)
	time.sleep(0.1)
	