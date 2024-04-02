import cv2
import math
import numpy as np

cam = cv2.VideoCapture(0)

while True:
	ret, image = cam.read()

	image = cv2.resize(image, (320, 240))
	imageb = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	img2 = cv2.Canny(imageb,110,200)

	#img = cv2.GaussianBlur(image,(5,5),0)

	#img = cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,2)
	
	hough = cv2.HoughLines(img2, 1, np.pi / 180, 90, None, 0, 0)

	if hough is not None:
		vtheta = []
		vrho = []
		for i in range(0,len(hough)):
			rho = hough[i][0][0]
			theta = hough[i][0][1]
			if theta > 3 * np.pi / 4 or theta < np.pi/4:
				vtheta.append(theta)
				vrho.append(rho)
				a = math.cos(theta)
				b = math.sin(theta)
				x0 = a * rho
				y0 = b * rho
				pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
				pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))

				cv2.line(image, pt1, pt2, (0, 0, 255), 3, cv2.LINE_AA)

		if len(vtheta) > 0:
			x = 0
			y = 0
			for angle in vtheta:
				x += math.cos(angle)
				y += math.sin(angle)
			midtheta = math.atan2(x, y)

			midrho = sum(vrho) / len(vrho)

			ba = math.cos(midtheta)
			bb = math.sin(midtheta)
			bx0 = ba * midrho
			by0 = bb * midrho
			bpt1 = (int(bx0 + 1000*(-bb)), int(by0 + 1000*(ba)))
			bpt2 = (int(bx0 - 1000*(-bb)), int(by0 - 1000*(ba)))

			cv2.line(image, bpt1, bpt2, (0, 255, 0), 3, cv2.LINE_AA)
	
	cv2.imshow('Lines',image)
	# cv2.imshow('canny',img2)
	

	k = cv2.waitKey(1)
	if k == 27:
		break
#cv2.imwrite('/home/pi/testimage.jpg', image)
cam.release()
cv2.destroyAllWindows()
