from cv2 import cv2
import numpy as np

img = cv2.imread("lines.png")
#getting the edges, by first converting the image to grayscale image
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 75, 150)
#houghline transform function
lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50)
#there is an additional variable called maxlinegap which fills the gaps if exist in the lines
for line in lines:
    #lines is an array of arrays, in which every array contains a line starting and ending points; x1,y1...etc
    x1,y1,x2,y2 =line[0]
    #accordingly x1,y1... are arrays of the starting and ending points of the lines
    cv2.line(img,(x1,y1),(x2,y2),(0,255,0),3) #draws a green line with a thickness equal to 3

cv2.imshow("edges",edges)
cv2.imshow("image",img)
cv2.waitKey(0)
cv2.destroyAllWindows()