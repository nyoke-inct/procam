# The following code is used to watch a video stream, detect Aruco markers, and use
# a set of markers to determine the posture of the camera in relation to the plane
# of markers.
#
# Assumes that all markers are on the same plane, for example on the same piece of paper
#
# Requires camera calibration (see the rest of the project for example calibration)

import numpy as np
import cv2
import cv2.aruco as aruco
import os
import pickle

# Check for camera calibration data
if not os.path.exists('./calibration/ProCamCalibration.pckl'):
    print("You need to calibrate the camera you'll be using. See calibration project directory for details.")
    exit()
else:
    f = open('./calibration/ProCamCalibration.pckl', 'rb')
    (proj_R, proj_T, projectorMatrix, projectorDistCoeffs, cameraMatrix, distCoeffs, ret) = pickle.load(f)
    f.close()
    if cameraMatrix is None or distCoeffs is None:
        print("Calibration issue. Remove ./calibration/ProCamCalibration.pckl and recalibrate your camera with CalibrateCamera.py.")
        exit()

def drawCube(img, corners, imgpts):
    imgpts = np.int32(imgpts).reshape(-1,2)

    # draw ground floor in green
    # img = cv2.drawContours(img, [imgpts[:4]],-1,(0,255,0),-3)

    # draw pillars in blue color
    for i,j in zip(range(4),range(4,8)):
        img = cv2.line(img, tuple(imgpts[i]), tuple(imgpts[j]),(255),3)

    # draw top layer in red color
    img = cv2.drawContours(img, [imgpts[4:]],-1,(0,0,255),3)

    return img

# Constant parameters used in Aruco methods
ARUCO_PARAMETERS = aruco.DetectorParameters_create()
ARUCO_DICT = aruco.Dictionary_get(aruco.DICT_5X5_50)

# Create grid board object we're using in our stream
board = aruco.GridBoard_create(
        markersX=1,
        markersY=1,
        markerLength=0.09,
        markerSeparation=0.01,
        dictionary=ARUCO_DICT)

# Create vectors we'll be using for rotations and translations for postures
rvecs, tvecs = None, None
axis = np.float32([[-.5,-.5,0], [-.5,.5,0], [.5,.5,0], [.5,-.5,0],
                   [-.5,-.5,1],[-.5,.5,1],[.5,.5,1],[.5,-.5,1] ])

# Make output image fullscreen
cv2.namedWindow('ProjectImage',cv2.WINDOW_NORMAL)
cv2.namedWindow('InputImage',cv2.WINDOW_NORMAL)
# cv2.setWindowProperty('ProjectImage', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
# cv2.resizeWindow('ProjectImage', 1280, 800)

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_AUTOFOCUS, 0)
cam.set(3, 1280)
cam.set(4, 720)
while(cam.isOpened()):
    # Capturing each frame of our video stream
    ret, ProjectImage = cam.read()
    if ret == True:
        # grayscale image
        gray = cv2.cvtColor(ProjectImage, cv2.COLOR_BGR2GRAY)

        # Display our image
        cv2.imshow('InputImage', ProjectImage)

        # Make background black
        ProjectImage = np.zeros((720, 1280, 3), np.uint8)
        
        # Detect Aruco markers
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, ARUCO_DICT, parameters=ARUCO_PARAMETERS)
  
        # Refine detected markers
        # Eliminates markers not part of our board, adds missing markers to the board
        corners, ids, rejectedImgPoints, recoveredIds = aruco.refineDetectedMarkers(
                image = gray,
                board = board,
                detectedCorners = corners,
                detectedIds = ids,
                rejectedCorners = rejectedImgPoints,
                cameraMatrix = cameraMatrix,
                distCoeffs = distCoeffs)   

        # Outline all of the markers detected in our image
        # ProjectImage = aruco.drawDetectedMarkers(ProjectImage, corners, ids, borderColor=(0, 0, 255))
        ProjectImage = aruco.drawDetectedMarkers(ProjectImage, corners, borderColor=(0, 0, 255))
        # ProjectImage = cv2.copyMakeBorder(ProjectImage,1000,1000,1500,1500,cv2.BORDER_CONSTANT,value=[0,0,0])

        # Draw the Charuco board we've detected to show our calibrator the board was properly detected
        # Require 15 markers before drawing axis
        if ids is not None and len(ids) > 0:
            # Estimate the posture per each Aruco marker
            rvecs, tvecs, _objPoints = aruco.estimatePoseSingleMarkers(corners, 1, cameraMatrix, distCoeffs)
            
            for rvec, tvec in zip(rvecs, tvecs):
                # project 3D points to image plane
                try:
                    imgpts, jac = cv2.projectPoints(axis, rvec, tvec, cameraMatrix, distCoeffs)
                except:
                    continue
                # ProjectImage = drawCube(ProjectImage, corners, imgpts)    
                ProjectImage = aruco.drawAxis(ProjectImage, cameraMatrix, distCoeffs, rvec, tvec, 1)

        cv2.imshow('ProjectImage', ProjectImage)

    # Exit at the end of the video on the 'q' keypress
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()