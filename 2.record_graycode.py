#!/usr/bin/env python3

'''
 graycodeパターンを投射して撮影する
'''
import time
from pathlib import Path
import cv2
import depthai as dai
import tkinter as tk
TkRoot = tk.Tk()

#ディスプレイサイズ取得
display_width = TkRoot.winfo_screenwidth()
display_height = TkRoot.winfo_screenheight()

print(f"{display_width} X {display_height}")

#ウィンドウをフルスクリーンに設定

# Change here
WIDTH = 1920
HEIGHT = 1080

# For secondary monitor,
LEFT = 500
TOP = 100

cv2.namedWindow('screen', cv2.WINDOW_NORMAL)
#cv2.moveWindow('screen', LEFT, TOP)
#cv2.setWindowProperty('screen', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
test = cv2.imread("./test.png")
cv2.imshow('screen', test)

cv2.waitKey(0) # キーが押されるまで待つ

# Create pipeline
pipeline = dai.Pipeline()

# Define sources and outputs
camRgb = pipeline.createColorCamera()
#videoEnc = pipeline.createVideoEncoder()
#xoutJpeg = pipeline.createXLinkOut()
xoutRgb = pipeline.createXLinkOut()

#xoutJpeg.setStreamName("jpeg")
xoutRgb.setStreamName("rgb")

# Properties
camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)
camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
#videoEnc.setDefaultProfilePreset(camRgb.getVideoSize(), camRgb.getFps(), dai.VideoEncoderProperties.Profile.MJPEG)

# Linking
camRgb.video.link(xoutRgb.input)
#camRgb.video.link(videoEnc.input)
#videoEnc.bitstream.link(xoutJpeg.input)

# Connect to device and start pipeline
with dai.Device(pipeline) as device:

    # Output queue will be used to get the rgb frames from the output defined above
    qRgb = device.getOutputQueue(name="rgb", maxSize=1, blocking=True)

    print('Connected cameras: ', device.getConnectedCameras())
    # Print out usb speed
    print('Usb speed: ', device.getUsbSpeed().name)

    # Make sure the destination path is present before starting to store the examples
    dirName = "rgb_data"
    Path(dirName).mkdir(parents=True, exist_ok=True)

    i = 0
    gcode_dir = "graycode_pattern"

    code_img = cv2.imread(f"{gcode_dir}/pattern_{str(i).zfill(2)}.png")
    cv2.imshow("screen", code_img)

    while True:
        code_img = cv2.imread(f"{gcode_dir}/pattern_{str(i).zfill(2)}.png")
        cv2.imshow("screen", code_img)

        if cv2.waitKey(1) == ord('q'):
            break
        
        time.sleep(2) #処理落ちがあるとイヤなので1秒だけまつ

        inRgb = qRgb.get()  # Non-blocking call, will return a new data that has arrived or None otherwise

        cv2.imwrite(f"{dirName}/pattern_{str(i).zfill(2)}.png", inRgb.getCvFrame())
        i = i + 1
        if i == 44:
            break
