#!/usr/bin/env python3

'''
 graycodeパターンを投射して撮影する
'''
import time
from pathlib import Path
import cv2
import depthai as dai

cv2.namedWindow('screen', cv2.WINDOW_NORMAL)
test = cv2.imread("./test.png")
cv2.imshow('screen', test)

cv2.waitKey(0) # キーが押されるまで待つ

# Create pipeline
pipeline = dai.Pipeline()

# Define source and output
camRgb = pipeline.createColorCamera()
xoutRgb = pipeline.createXLinkOut()

xoutRgb.setStreamName("rgb")

# Properties
camRgb.setPreviewSize(1920, 1080)
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
    qRgb = device.getOutputQueue(name="rgb", maxSize=1, blocking=False)
 
    # Make sure the destination path is present before starting to store the examples
    dirName = "rgb_data"
    Path(dirName).mkdir(parents=True, exist_ok=True)

    i = 0
    gcode_dir = "graycode_pattern"

    code_img = cv2.imread(f"{gcode_dir}/pattern_{str(i).zfill(2)}.png")
    cv2.imshow("screen", code_img)

    cv2.waitKey(0)


    device.getQueueEvents()

    while True:
        code_img = cv2.imread(f"{gcode_dir}/pattern_{str(i).zfill(2)}.png")
        cv2.imshow("screen", code_img)
        img = qRgb.get()

        cv2.waitKey(0)
        time.sleep(1)

        img = qRgb.get()

        if cv2.waitKey(1) == ord('q'):
            break

        cv2.imwrite(f"{dirName}/pattern_{str(i).zfill(2)}.png", img.getCvFrame())
        i = i + 1
        if i == 44:
            break
