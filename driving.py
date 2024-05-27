import serial
import cv2
import math
import numpy as np
import time

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.reset_input_buffer()

linesnum = 2

red = (0, 0, 255)
blue = (255, 0, 0)
green = (0, 255, 0)

blindtime = 25

nextturn = 0
count = 0

def lines(theta, rho, colour, transform):

	a = math.cos(theta)
	b = math.sin(theta)

	x0 = (a * rho) + transform
	y0 = (b * rho)
	
	pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
	pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))

	cv2.line(image, pt1, pt2, colour, 3, cv2.LINE_AA)

	return(x0, y0)

def linesseperate(t1, t2, threshold, VorH):
	
	if VorH == 'V':
		n1 = t1 + np.pi/2
		n2 = t2 + np.pi/2
	else:
		n1 = t1
		n2 = t2

	if n1/n2 >= 1-threshold and n1/n2 <= 1+threshold:
		return False
	
	else:
		return True

def rhoseperate(r1, r2, threshold):

	if abs(abs(r1) - abs(r2)) >= threshold:
		return True
	else:
		return False

def arduino(message):
	try:
		ser.write(message)
		ser.write(b"\n")
	except:
		print("cant connect to arduino")
	#time.sleep(0.001)

def midroad(t1, r1, t2, r2):

	x = (r2*np.sin(t1) - r1*np.sin(t2))/(np.sin(t1)*np.cos(t2) - np.sin(t2)*np.cos(t1))

	if not np.isnan(x):
		cv2.circle(image,(int(x),63), 5, (255,0,150), -1)

	if x == 320: 
		direction = 0
	else:
		direction = (x-320) / 10
	return direction

def turn(direction):
	pass

while True:
	ret, image = cap.read()

	image = cv2.rotate(image, cv2.ROTATE_180)

	img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	
	img = cv2.GaussianBlur(img,(5,5),0)
	img = cv2.Canny(img,50,160)

	Limg = img[0:480, 0:300]
	Rimg = img[0:480, 340:640]
	
	hough = cv2.HoughLines(img, 2, np.pi / 135, 70, None, 0, 0)
	Lhough = cv2.HoughLines(Limg, 2, np.pi / 135, 70, None, 0, 0)
	Rhough = cv2.HoughLines(Rimg, 2, np.pi / 135, 70, None, 0, 0)

	#print(count)
	roaddirection = 0
	
	if hough is not None:

		vtheta = []
		vrho = []

		for i in range(0,len(hough)):

			rho = hough[i][0][0]
			theta = hough[i][0][1]

			if theta > 3*np.pi/4 or theta < np.pi/4:

				vtheta.append(theta)
				vrho.append(rho)

		if len(vtheta) > linesnum:

			nextgood = 0
			i = 1
			
			while nextgood == 0 and i < len(vtheta):

				if linesseperate(vtheta[0], vtheta[i], 0.05, 'V'):
					nextgood = i
				
				i += 1
			
			if nextgood != 0:

				lines(vtheta[0], vrho[0], red, 0)
				lines(vtheta[nextgood], vrho[nextgood], red, 0)		

				roaddirection = -1*(midroad(vtheta[0], vrho[0], vtheta[nextgood], vrho[nextgood]))
				
				count = 0

			else:
				count += 1
		else:
			count += 1
	
	if Lhough is not None:
	
		htheta1 = []
		hrho1 = []

		for i in range(0,len(Lhough)):

			rho = Lhough[i][0][0]
			theta = Lhough[i][0][1]

			if theta < 3*np.pi/4 and theta > np.pi/4:

				htheta1.append(theta)
				hrho1.append(rho)

		if len(htheta1) > linesnum:

			nextgood1 = 0
			i = 1
		
			while nextgood1 == 0 and i < len(htheta1):

				if not linesseperate(htheta1[0], htheta1[i], 0.2, 'H') and rhoseperate(hrho1[0], hrho1[i], 50):
					nextgood1 = i
				
				i += 1
			if nextgood1 != 0:
				lines(htheta1[0], hrho1[0], green, 0)
				lines(htheta1[nextgood1], hrho1[nextgood1], green, 0)

				nextturn -= 1
	
	if Rhough is not None:

		htheta2 = []
		hrho2 = []

		for i in range(0,len(Rhough)):

			rho = Rhough[i][0][0]
			theta = Rhough[i][0][1]

			if theta < 3*np.pi/4 and theta > np.pi/4:

				htheta2.append(theta)
				hrho2.append(rho)

		if len(htheta2) > linesnum:

			nextgood2 = 0
			i = 1
			
			while nextgood2 == 0 and i < len(htheta2):

				if not linesseperate(htheta2[0], htheta2[i], 0.2, 'H') and rhoseperate(hrho2[0], hrho2[i], 50):
					nextgood2 = i
				
				i += 1

			if nextgood2 != 0:
				lines(htheta2[0], hrho2[0], blue, 340)
				lines(htheta2[nextgood2], hrho2[nextgood2], blue, 340)		

				nextturn += 1

		if count >= blindtime:
			if nextturn < -2:
				arduino(b"-100")
				print(roaddirection, " -100")
			elif nextturn > 2:
				arduino(b"100")
				print(roaddirection, "100")
			else:
				arduino(b"-100")
				print(roaddirection, " -100")
		else:
			number = str(roaddirection)
			print(number)
			numberb = bytes(number, 'utf-8')
			arduino(numberb)
			
		


	cv2.imshow('Lines',image)
	cv2.imshow('lcanny',Limg)
	cv2.imshow('canny',Rimg)

	k = cv2.waitKey(1)
	if k == 27:
		break
	if k == 27:
		break
	#0.001-0.01

cap.release()
cv2.destroyAllWindows()