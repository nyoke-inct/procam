#!/usr/bin/env python3

import cv2
import depthai as dai
import tkinter as tk
TkRoot = tk.Tk()
import numpy as np


#ディスプレイサイズ取得
display_width = TkRoot.winfo_screenwidth()
display_height = TkRoot.winfo_screenheight()
print(f"{display_width} X {display_height}")

#ウィンドウをフルスクリーンに設定
# Change here
WIDTH = 1280
HEIGHT = 720

# For secondary monitor,
#LEFT = 500
#TOP = 100

#cv2.namedWindow('screen', cv2.WINDOW_AUTOSIZE)
cv2.namedWindow('screen', cv2.WINDOW_NORMAL)
#cv2.moveWindow('screen', LEFT, TOP)
cv2.setWindowProperty('screen', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
test = cv2.imread("./test.png")
print(test.shape[:3])
cv2.drawMarker(test, (10, 10), (0, 0, 255))
cv2.drawMarker(test, (1270, 10), (0, 0, 255))
cv2.drawMarker(test, (10, 710), (0, 0, 255))
cv2.drawMarker(test, (1270, 710), (0, 0, 255))



cv2.imshow('screen', test)

#ディスプレイサイズ取得
display_width = TkRoot.winfo_screenwidth()
display_height = TkRoot.winfo_screenheight()
print(f"{display_width} X {display_height}")

cv2.waitKey(0) # キーが押されるまで待つ

# Create pipeline
pipeline = dai.Pipeline()

# Define source and output
camRgb = pipeline.createColorCamera()
xoutRgb = pipeline.createXLinkOut()

xoutRgb.setStreamName("rgb")

# Properties
camRgb.setPreviewSize(1280, 720)
camRgb.setInterleaved(False)
camRgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)

# Linking
camRgb.preview.link(xoutRgb.input)

# Connect to device and start pipeline
with dai.Device(pipeline) as device:

    print('Connected cameras: ', device.getConnectedCameras())
    # Print out usb speed
    print('Usb speed: ', device.getUsbSpeed().name)

    # Output queue will be used to get the rgb frames from the output defined above
    qRgb = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)

    while True:
        inRgb = qRgb.get()  # blocking call, will wait until a new data has arrived

        # Retrieve 'bgr' (opencv format) frame
        cv2.imshow("screen", inRgb.getCvFrame())

        if cv2.waitKey(1) == ord('q'):
            break
