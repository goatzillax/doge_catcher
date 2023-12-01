import cv2
import numpy as np
import sys

image = cv2.imread(sys.argv[1])

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV);  #  colorspace conversion

lower = np.array([57, 130, 129])  #  I don't know why the image guys have to do shit like this
upper = np.array([90, 255, 255])

mask = cv2.inRange(hsv, lower, upper)  #  I guess this applies some sort of threshold to the hsv space image
specific_color_img = cv2.bitwise_and(image, image, mask=mask)  #  applies the mask

#  ok now find contours on the specific_color_img and extract all the rectangles.

#  Fucking pedantic
imgray = cv2.cvtColor(specific_color_img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(imgray, 64, 255, cv2.THRESH_BINARY)

contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

idx = 0;
for cnt in contours:  #  uh, quagmire, doesn't country have an 'o' in it?
   x, y, w, h = cv2.boundingRect(cnt)

   #  uh let's set some reasonable limits for like a minimum size doggo aight?
   if (w < 10 or h < 10):
      continue
   crop = image[y:y + h, x:x+w]
   #cv2.imshow("eat shit", crop);
   #cv2.waitKey()
   cv2.imwrite("%s-%d.png" % (sys.argv[1][:-4], idx), crop);
   idx += 1


