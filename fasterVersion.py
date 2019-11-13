from cv2 import cv2
import numpy as np
import scipy.ndimage as ndi
import matplotlib.pyplot as plt
from PIL import Image
import time
import requests
import _thread
import urllib.request
from threading import Thread
import logging
import queue

result=queue.Queue()
from firebase import firebase
firebase=firebase.FirebaseApplication('https://carcontroller-76535.firebaseio.com/',None)



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
    height,width=Gray.shape
    print(height,width)
    mask=np.zeros_like(Gray)
    cv2.rectangle(mask,(60,50),(width-100,height),(255,255,255),-1)
    masked_image=cv2.bitwise_and(Gray,mask)

    #cv2.imshow("mask",masked_image)
    #cv2.waitKey()
    return masked_image


def showImage(image_lines,gray_lines,filter):
    #with_objects=Countour_detection(img,Gray_scaled_image)
    cv2.namedWindow("image_with_lines",cv2.WINDOW_NORMAL)
    cv2.resizeWindow("image_with_lines",200,200)
    cv2.imshow("image_with_lines",image_lines)
    cv2.namedWindow("Filtered_image",cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Filtered_image",200,200)
    cv2.imshow("Filtered_image",filter)
    cv2.namedWindow("Gray_scale_with_lines",cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Gray_scale_with_lines",200,200)
    cv2.imshow("Gray_scale_with_lines",gray_lines)

    #cv2.imshow("with_objects",with_objects)
    cv2.waitKey(1)



def showPlottedImage(Gray_image):
    plt.imshow(Gray_image)
    plt.show()



def houghline_transform(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    Gray_scaled_image=Gray_image(hsv)
    filtered_image=region_of_interest(img,Gray_scaled_image)
    lines = cv2.HoughLinesP(Gray_scaled_image, 1, np.pi/180, 50)
    #print(lines)
    for line in lines:
     #lines is an array of arrays, in which every array contains a line starting and ending points; x1,y1...etc
        x1,y1,x2,y2 =line[0]
    #accordingly x1,y1... are arrays of the starting and ending points of the lines
        cv2.line(Gray_scaled_image,(x1,y1),(x2,y2),(255,255,255),6) #draws a green line with a thickness equal to 3
        cv2.line(img,(x1,y1),(x2,y2),(255,0,0),6) #draws a green line with a thickness equal to 3
    #with_objects=Countour_detection(img,Gray_scaled_image)
    #showImage(img,Gray_scaled_image,filtered_image)

    result.put(lines)
    #showPlottedImage(Gray_scaled_image)
    return lines

    #showPlottedImage(Gray_scaled_image)


#make coordinates function, takes the slopes and return the coor
def make_points(frame, line):
    height, width, _ = frame.shape
    slope, intercept = line
    y1 = height  # bottom of the frame
    y2 = int(y1 * 1 / 2)  # make points from middle of the frame down

    # bound the coordinates within the frame
    x1 = max(-width, min(2 * width, int((y1 - intercept) / slope)))
    x2 = max(-width, min(2 * width, int((y2 - intercept) / slope)))
    return [[x1, y1, x2, y2]]


def average_slope_intercept(frame, line_segments):
    """
    This function combines line segments into one or two lane lines
    If all line slopes are < 0: then we only have detected left lane
    If all line slopes are > 0: then we only have detected right lane
    """
    lane_lines = []
    if line_segments is None:
        print('No line_segment segments detected')
        return lane_lines

    height, width, _ = frame.shape
    left_fit = []
    right_fit = []

    boundary = 1/3
    left_region_boundary = width * (1 - boundary)  # left lane line segment should be on left 2/3 of the screen
    right_region_boundary = width * boundary # right lane line segment should be on left 2/3 of the screen

    for line_segment in line_segments:
        for x1, y1, x2, y2 in line_segment:
            if x1 == x2:
                continue
            fit = np.polyfit((x1, x2), (y1, y2), 1)
            slope = fit[0]
            intercept = fit[1]
            if slope < 0:
                if x1 < left_region_boundary and x2 < left_region_boundary:
                    left_fit.append((slope, intercept))
            else:
                if x1 > right_region_boundary and x2 > right_region_boundary:
                    right_fit.append((slope, intercept))
            if left_fit and right_fit:
                control=firebase.put('SteeringWheel',str('forward'), 2 )
                control=firebase.put('SteeringWheel',str('left'), 0 )
                control=firebase.put('SteeringWheel',str('reverse'), 0 )
                control=firebase.put('SteeringWheel',str('right'), 0 )
                print('both lines')
            elif left_fit:
                control=firebase.put('SteeringWheel',str('forward'), 2 )
                control=firebase.put('SteeringWheel',str('left'), 0 )
                control=firebase.put('SteeringWheel',str('right'), 2 )
                control=firebase.put('SteeringWheel',str('reverse'), 0 )
                print('left line')
            elif right_fit:
                control=firebase.put('SteeringWheel',str('left'), 2 )
                control=firebase.put('SteeringWheel',str('forward'), 2 )
                control=firebase.put('SteeringWheel',str('right'),  0)
                control=firebase.put('SteeringWheel',str('reverse'), 0 )
                print('right line')
    ''''
    left_fit_average = np.average(left_fit, axis=0)
    if len(left_fit) > 0:
        lane_lines.append(make_points(frame, left_fit_average))

    right_fit_average = np.average(right_fit, axis=0)
    if len(right_fit) > 0:
        lane_lines.append(make_points(frame, right_fit_average))
    '''''

    #for line in lane_lines:
     #lines is an array of arrays, in which every array contains a line starting and ending points; x1,y1...etc
       # x1,y1,x2,y2 =line[0]
    #accordingly x1,y1... are arrays of the starting and ending points of the lines
        #cv2.line(frame,(x1,y1),(x2,y2),(255,255,255),3)
    #return lane_lines

    #cv2.imshow("AVG_LINE",frame)
    #cv2.waitKey(1)



def webCam ():

     url = "http://172.28.131.139:8080/shot.jpg"
     cv2.namedWindow("ipcam",cv2.WINDOW_NORMAL)
     cv2.resizeWindow("ipcam",200,200)

     while True:
      imgRes=urllib.request.urlopen(url)
      imgArray= np.array(bytearray(imgRes.read()),dtype=np.uint8)
      img =cv2.imdecode(imgArray,-1)
      cv2.imshow("ipcam",img)
      LINES=Thread(target= houghline_transform, args=(img,))
      LINES.start()
      #ret=LINES.join()
      ret=result.get()
      #print(ret)
      #LINES=houghline_transform(img)
      img2=np.copy(img)
      #average_slope_intercept(img2,LINES)
      _thread.start_new_thread( average_slope_intercept, (img2, ret, ) )

      if cv2.waitKey(1)==27:
          break
webCam()




