from cv2 import cv2
import numpy as np
import scipy.ndimage as ndi
import matplotlib.pyplot as plt
from PIL import Image
import time



def Gray_image(image):
  #getting the edges, by first converting the image to grayscale image
   gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  #apply gaussian filter, using 5x5 kernel
   blur=cv2.GaussianBlur(gray,(5,5),0)
  #getting edges, second argument is the low_threshold, followed by the high one
   edges = cv2.Canny(blur, 75, 150)
  #houghline transform function
   return edges
   
def region_of_interest(image,Gray):
    #height,width,channels=image.shape
    mask=np.zeros_like(Gray)
    cv2.rectangle(mask,(0,240),(600,350),(255,255,255),-1)
    masked_image=cv2.bitwise_and(Gray,mask)
    #cv2.imshow("mask",masked_image)
    #cv2.waitKey()
    return masked_image
#shows the image using CV2
def showImage(Gray_image,Normal_image):
    cv2.imshow("edges",Gray_image)
    cv2.imshow("image",Normal_image)
    cv2.waitKey()

def showPlottedImage(Gray_image):
    plt.imshow(Gray_image)
    plt.show()

def houghline_transform(img): 
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    Gray_scaled_image=Gray_image(hsv)
    filtered_image=region_of_interest(img,Gray_scaled_image)
    #cv2.imshow("IMAGE",img)
    lines = cv2.HoughLinesP(filtered_image, 1, np.pi/180, 50, maxLineGap=100)
    print(lines)
#there is an additional variable called maxlinegap which fills the gaps if exist in the lines
    for line in lines:
     #lines is an array of arrays, in which every array contains a line starting and ending points; x1,y1...etc
        x1,y1,x2,y2 =line[0]
    #accordingly x1,y1... are arrays of the starting and ending points of the lines
        cv2.line(Gray_scaled_image,(x1,y1),(x2,y2),(255,255,255),6) #draws a green line with a thickness equal to 3
        cv2.line(img,(x1,y1),(x2,y2),(255,0,0),6) #draws a green line with a thickness equal to 3
         

    cv2.imshow("IMAGE",img)
    cv2.imshow("Filtered_image",filtered_image)
    cv2.imshow("Gray_scale_with_lines",Gray_scaled_image)
    cv2.waitKey(1)



img = cv2.imread("image1.jpeg")
#Gray_scaled_image=Gray_image(img)
#new_Gray_image=np.copy(Gray_scaled_image)


##FUNCTION##
#houghline_transform(img)
#showImage(hsv,Gray_scaled_image) 
#showPlottedImage(Gray_scaled_image)

##Video stuff
cap=cv2.VideoCapture("test.mp4")
'''
ret, frame = cap.read()
#cv2.imshow('Frame',frame)
houghline_transform(frame)
'''
while (cap.isOpened()):
    _,frame=cap.read()
    houghline_transform(frame)
    time.sleep(1)
