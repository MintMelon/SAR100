import cv2
import numpy as np


def callback(x):
    pass


cv2.namedWindow('Image')

ref_point = [(0, 800)]
idx = 0


# Mouse Events
def shape_selection(event, x, y, flags, param):
    global ref_point, idx, drawing, point1, point2
    if event == cv2.EVENT_LBUTTONDOWN:
        ref_point = [(x, y)]
        print (ref_point)
        print (image[ref_point[0][1], ref_point[0][0]])

        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        cv2.imshow("hsv", hsv)
        d = hsv.item(y, x, 0)
        e = hsv.item(y, x, 1)
        f = hsv.item(y, x, 2)
        print("DEF", d, e, f)
        if (d + 20 >= 360):
            dup = 360
        else:
            dup = d+ (360-d)

        if (d - 20 <= 0):
            dlow = 0
        else:
            dlow = d-d


        #print(dup, dlow, eup, elow, fup, flow)
        lower_color = np.array([dlow, 60, 60])
        upper_color = np.array([dup, 255, 255])

        mask = cv2.inRange(hsv, lower_color, upper_color)
        # cv2.imshow('Mask', mask)

        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        for contour in contours:
            if (cv2.pointPolygonTest(contour, ref_point[0], False)) == 1:
                print("point is inside contour")
                cv2.drawContours(image, contour, -1, (0, 255, 0), 3)

                # Centre Calculation
                M = cv2.moments(contour)
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                centre = (cx, cy)
                print(centre)

                # Saving Image
                a, b, w, h = cv2.boundingRect(contour)
                if w > 50 and h > 50:
                    idx += 1
                    new_img = image_1[b:b + h, a:a + w]
                    cv2.imwrite(str(idx) + '.png', new_img)

        cv2.imshow("Image", image)


cv2.setMouseCallback("Image", shape_selection)

# Image Reading
image = cv2.imread("Pics/leaves2.jpg")
#blurred_image = cv2.GaussianBlur(image, (5, 5), 1)
image_1= cv2.imread("Pics/leaves2.jpg")

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

print(image.shape)

cv2.imshow("Image", image)

cv2.waitKey(0)
cv2.destroyAllWindows()
