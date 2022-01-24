''' カメラで机に置いたARマーカーを写し，それをマウスで順にクリックすることで射影変換の行列を得る '''
import cv2
from cv2 import aruco
import numpy as np
import random

ARUCO_DICT = aruco.Dictionary_get(aruco.DICT_4X4_50)

def draw_quadrangle(event, x, y, flags, param):
    img = param["img"]
    pts = param["pts"]
    pic = param["pic"]

    color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
    img_tmp = img.copy()

    if event == cv2.EVENT_MOUSEMOVE and len(pts) <= 3:
        h, w = img.shape[:2]
        cv2.line(img_tmp, (x,0), (x,h-1), color)
        cv2.line(img_tmp, (0,y), (w-1,y), color)        
        cv2.imshow("image", img_tmp)

    if event == cv2.EVENT_LBUTTONDOWN:
        pts.append((x, y))
        if len(pts) == 4:
            h, w = img.shape[:2]
            ph, pw = pic.shape[:2]
            pts1 = np.float32(pts)
            pts2 = np.float32([[0,0],[0,ph],[pw,ph],[pw,0]])

            M1 = cv2.getPerspectiveTransform(pts1,pts2)
            tmp = cv2.warpPerspective(img,M1,(pw,ph))
            #cv2.imwrite("cut_image.jpg", tmp)

            M2 = cv2.getPerspectiveTransform(pts2,pts1)
            transparence = (128,128,128)
            front = cv2.warpPerspective(pic, M2, (w,h), borderValue=transparence)
            img = np.where(front==transparence, img, front)
            #cv2.imwrite("front.jpg", front)
            cv2.imshow("image", img)
            #cv2.imwrite("image.jpg", img)

    if event == cv2.EVENT_RBUTTONDOWN and len(pts)>0:
        del pts[-1]

    if 0 < len(pts) <= 3:
        for pos in pts:
            cv2.circle(img_tmp, pos, 5, (0,0,255), -1)

        cv2.line(img_tmp, pts[-1], (x,y), color, 1)
        if len(pts)==3:
            cv2.line(img_tmp, pts[0], (x,y), color, 1)

        isClosed = True if len(pts)==4 else False
        cv2.polylines(img_tmp, [np.array(pts)], isClosed, (0,0,255), 1)
        cv2.imshow("image", img_tmp)

def main():
    img_origin = cv2.imread("test1.png")
    pic = cv2.imread("test2.png")
    pts = []
    cv2.imshow("image", img_origin)
    cv2.setMouseCallback("image", draw_quadrangle, param={"img":img_origin, "pts":pts, "pic":pic})

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()