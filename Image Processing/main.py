import cv2
import numpy as np

def callback(x):
	pass

cv2.namedWindow('Image')

ref_point= [(0, 800)]
idx = 0

# Mouse Events
def shape_selection(event, x, y, flags, param):
	global ref_point, idx, drawing, point1, point2
	if event == cv2.EVENT_LBUTTONDOWN:
		ref_point = [(x, y)]
		print (ref_point)
		print (image[ref_point[0][1], ref_point[0][0]])

		
     
cv2.setMouseCallback("Image", shape_selection)


# Image Reading
image = cv2.imread("Pics/leaves2.jpg")
blurred_image = cv2.GaussianBlur(image, (5, 5), 1)    
image_1 = cv2.imread("Pics/leaves2.jpg")

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)    

print(image.shape)

cv2.imshow("Image", image)


cv2.waitKey(0)
cv2.destroyAllWindows()
