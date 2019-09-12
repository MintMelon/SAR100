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

        img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV_FULL)

        # Filter out low saturation values, which means gray-scale pixels(majorly in background)
        bgd_mask = cv2.inRange(img_hsv, np.array([0, 0, 0]), np.array([180, 60, 255]))
        #cv2.imshow("ABC",bgd_mask)

        # Get a mask for pitch black pixel values
        black_pixels_mask = cv2.inRange(image, np.array([0, 0, 0]), np.array([70, 70, 70]))
        #cv2.imshow("BC", black_pixels_mask)

        # Get the mask for extreme white pixels.
        white_pixels_mask = cv2.inRange(image, np.array([230, 230, 230]), np.array([255, 255, 255]))
        ## cv2.imshow("C", white_pixels_mask)
        
        final_mask = cv2.max(bgd_mask, black_pixels_mask)
        final_mask = cv2.min(final_mask, ~white_pixels_mask)
        final_mask = ~final_mask
        #cv2.imshow("CA", final_mask)
        final_mask = cv2.erode(final_mask, np.ones((3, 3), dtype=np.uint8))
        final_mask = cv2.dilate(final_mask, np.ones((5, 5), dtype=np.uint8))


        contours, _ = cv2.findContours(final_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

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
image = cv2.imread("Pics/1017.jpg")
blurred_image = cv2.GaussianBlur(image, (5, 5), 1)
image_1 = cv2.imread("Pics/1017.jpg")

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

print(image.shape)

cv2.imshow("Image", image)

cv2.waitKey(0)
cv2.destroyAllWindows()
