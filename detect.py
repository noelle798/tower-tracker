import numpy as np
import cv2

cap = cv2.VideoCapture(2)

ret, image = cap.read()
height, width, depth = image.shape

color_hsv = [[85, 60, 175], [200, 255, 255]]

lower = np.array(color_hsv[0], dtype = "uint8")
upper = np.array(color_hsv[1], dtype = "uint8")

while(cv2.waitKey(1) & 0xFF != ord('q')):
	# capture and resize image
	ret, image = cap.read()

	# convert image from rgb to HSV
	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

	# find the colors within the specified boundaries and apply the mask
	mask = cv2.inRange(hsv, lower, upper)
	masked = cv2.bitwise_and(image, image, mask = mask)

	# show images
	cv2.imshow('image', np.hstack([image, masked]))

	# erode and dilate
	# kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
	# # opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
	# erosion = cv2.erode(mask, kernel, iterations = 1)
	# dilation = cv2.dilate(erosion, kernel, iterations = 2)
	# cv2.imshow("open", dilation)

	# find and display contours
	(contours, hierarchy) = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	contours = sorted(contours, key = cv2.contourArea, reverse = True)[:3]
	# cv2.drawContours(image, contours, -1, (0,0,255), 2)
	# cv2.imshow('contours', image)

	# match to u-shape
	# draw u-shape
	control = np.zeros((68, 100, 3), np.uint8)
	cv2.rectangle(control, (10, 10), (18, 58), (255, 255, 255), -1)
	cv2.rectangle(control, (18, 51), (82, 58), (255, 255, 255), -1)
	cv2.rectangle(control, (82, 10), (90, 58), (255, 255, 255), -1)
	control_gray = cv2.cvtColor(control, cv2.COLOR_BGR2GRAY)
	(control_contours, hierarchy) = cv2.findContours(control_gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cv2.drawContours(control, control_contours[0], -1, [0, 0, 255], 3)
	cv2.imshow('control cont', control)

	# # convex hull
	# for contour in contours:
	# 	hull = cv2.convexHull(contour)
	# 	for point in hull:
	# 		cv2.circle(image, tuple(point[0]), 3, [0, 255, 0], -1)
	#
	# cv2.imshow('convex hull', image)

	for cnt in contours:
		peri = cv2.arcLength(cnt, True)
		approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
		ret = cv2.matchShapes(control_contours[0], approx, 1, 0.0)
		if ret < 30:
			cv2.drawContours(image, approx, -1, [0,0,255], 3)
			cv2.imshow("img", image)
			print ret

	# approximate polygon
	# for cnt in contours:

		# peri = cv2.arcLength(cnt, True)
		# approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
		#
		# # if found something that might be tape
		# if len(approx) == 8:
		# 	tape = approx
		#
		# 	# display image of apparent tape
		# 	cv2.drawContours(image, tape, -1, [0, 0, 255], 5)
		# 	cv2.imshow("tape", image)
		#
		# 	# split points into four vertical lines
		# 	print "tape:", tape
		# 	# [[],[],[]...]
		# 	print "indices:", tape[:,0].argsort()
		# 	print "sorted tape:", tape[tape[:,0].argsort()]

	# convert image to grayscale and use canny edge detection
	# gray = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
	# edges = cv2.Canny(gray, 225, 250)
	# cv2.imshow('canny', edges)

cap.release()
cv2.destroyAllWindows()
