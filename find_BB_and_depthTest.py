import numpy as np
import cv2

# takes in a rgbd 4 dimensional image
def find_BB_and_depth(img_rgb, pixel_depths, drawContours = False):
    img = cv2.pyrDown(img_rgb)

    ret, threshed_img = cv2.threshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 127, 255, cv2.THRESH_BINARY)
    image, contours, hier = cv2.findContours(threshed_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    output = np.zeros([len(contours), 5])

    bbnum = 0

    listOfBBs = []

    for i in range(len(contours)):
        # get the bounding rect
        x, y, w, h = cv2.boundingRect(contours[i])

        if i == bbnum :
            # draw a green rectangle to visualize the bounding rect
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        depth = np.mean(pixel_depths[2 * y:2 * (y + h), 2 * x:2 * (x + w)])
        if w > 15 and h > 15 and w < 300 and h < 200:
            output[i, :] = x * 2, y * 2, w * 2, h * 2, depth
            listOfBBs.append(i)

    cv2.destroyAllWindows()

    print(listOfBBs)

    for i in listOfBBs:
        img = cv2.pyrDown(img_rgb)

        ret, threshed_img = cv2.threshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 127, 255, cv2.THRESH_BINARY)
        image, contours, hier = cv2.findContours(threshed_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # get the bounding rect
        x, y, w, h = cv2.boundingRect(contours[i])

        # draw a green rectangle to visualize the bounding rect
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow("contours", img)
        cv2.waitKey(10)

        raw_input("Current bbnum: " + str(i) + " Enter for next bb.")
        cv2.destroyAllWindows()

    return output
    # the type is a [k, 5] array, the 5 features are x, y, w, h, depth_of_bb_in_meters