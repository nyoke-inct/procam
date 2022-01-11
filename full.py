#!/usr/bin/env python3

import cv2
import depthai as dai
import tkinter as tk
import numpy as np
#from screeninfo import get_monitors
import tkinter as tk
from PIL import ImageGrab


root = tk.Tk()
resolution_width = root.winfo_screenwidth()
resolution_height = root.winfo_screenheight()

image = ImageGrab.grab()
real_width, real_height = image.width, image.height

ratio_width = real_width / resolution_width
ratio_height = real_height/ resolution_height

print(f"resolution: {resolution_width} X {resolution_height}")
print(f"real size : {real_width} X {real_height}")
print(f"ratio size: {ratio_width} X {ratio_height}")

#for m in get_monitors():
#   print(str(m))

cv2.namedWindow('screen', cv2.WINDOW_KEEPRATIO | cv2.WINDOW_NORMAL)
#cv2.setWindowProperty('screen', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# ディスプレイ解像度と同じサイズの配列を生成（黒色の画像）
img = np.zeros((resolution_height, resolution_width, 3), dtype=np.uint8) 

cv2.circle(img, (10, 10), 5, (0, 0, 255))
cv2.circle(img, (resolution_width-10, 10), 5, (0, 0, 255))
cv2.circle(img, (10, resolution_height-10), 5, (0, 0, 255))
cv2.circle(img, (resolution_width-10, resolution_height-10), 5, (0, 0, 255))

cv2.imshow('screen', img)

cv2.waitKey(0)
