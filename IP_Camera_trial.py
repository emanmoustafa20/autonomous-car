import requests
from cv2 import cv2
import numpy as np

url = "http://192.168.1.3:8080/shot.jpg"

while True:
    imgRes= requests.get(url)
    imgArray= np.array(bytearray(imgRes.content),dtype=np.uint8)
    img =cv2.imdecode(imgArray,-1)
    cv2.imshow("ipcam",img)
    cv2.namedWindow("ipcam", cv2.WINDOW_NORMAL)
    if cv2.waitKey(1)==27:
         break 
