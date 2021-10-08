#
#       Shape Detection test
#                   By; Jhon Tabio

from PIL import ImageGrab

import cv2
import win32gui as win
import numpy as np

font = cv2.FONT_HERSHEY_SIMPLEX

def screen_grab(version):
    # Search for a window with the title of Paint
    hwnd = win.FindWindow(None, "Test_Image - Paint")

    # Store window dimension
    dimensions = win.GetWindowRect(hwnd)
    addDimensions = (10, 152, -25, -50)
    newDimension = tuple(map(sum, zip(dimensions, addDimensions)))

    # Capture the frame
    image = ImageGrab.grab(newDimension)

    # Convert image into NP Array
    return np.array(image)
    

if __name__ == "__main__":
    print("Running...")
    
    version = 1

    cv2.namedWindow("Scroll Bars")
    cv2.createTrackbar("white", "Scroll Bars", 255, 255, lambda x: None)
    cv2.createTrackbar("black", "Scroll Bars", 150, 255, lambda x: None)

    cv2.createTrackbar("l_h", "Scroll Bars", 0, 180, lambda x: None)
    cv2.createTrackbar("l_s", "Scroll Bars", 0, 255, lambda x: None)
    cv2.createTrackbar("l_v", "Scroll Bars", 0, 255, lambda x: None)

    cv2.createTrackbar("h_h", "Scroll Bars", 180, 180, lambda x: None)
    cv2.createTrackbar("h_s", "Scroll Bars", 255, 255, lambda x: None)
    cv2.createTrackbar("h_v", "Scroll Bars", 255, 255, lambda x: None)
    
    while True:
        white = cv2.getTrackbarPos("white", "Scroll Bars")
        black = cv2.getTrackbarPos("black", "Scroll Bars")

        l_h = cv2.getTrackbarPos("l_h", "Scroll Bars")
        l_s = cv2.getTrackbarPos("l_s", "Scroll Bars")
        l_v = cv2.getTrackbarPos("l_v", "Scroll Bars")

        h_h = cv2.getTrackbarPos("h_h", "Scroll Bars")
        h_s = cv2.getTrackbarPos("h_s", "Scroll Bars")
        h_v = cv2.getTrackbarPos("h_v", "Scroll Bars")
        
        frame_np = screen_grab(version)
        
        if version == 0:
            # Display in full colors
            frame = cv2.cvtColor(frame_np, cv2.COLOR_RGB2BGR)
        elif version == 1:
            # Display in grayscale
            frame =  cv2.cvtColor(frame_np, cv2.COLOR_BGR2GRAY)
        elif version == 2:
            frame = cv2.cvtColor(frame_np, cv2.COLOR_BGR2LAB)
        else:
            # Displays all the outlines
            frame = cv2.Canny(frame_np, 100, 100)
        
        cv2.imshow("Analyze Screen", frame)

        hsv =  cv2.cvtColor(frame_np, cv2.COLOR_BGR2HSV)

        red_lower_range = np.array([110, 25, 0])
        red_higher_range = np.array([179, 255, 255])
        red_mask = cv2.inRange(hsv, red_lower_range, red_higher_range)
        cv2.imshow("Red Mask", red_mask)

        lower_range = np.array([l_h, l_s, l_v])
        higher_range = np.array([h_h, h_s, h_v])
        mask = cv2.inRange(hsv, lower_range, higher_range)
        cv2.imshow("General Mask", mask)

        # OLD METHOD, MOVING TO COLOR DETECTION TO HOPEFULLY DIFFERENTIATE SHAPES AND MIX OF SHAPES
        ret, thresh = cv2.threshold(cv2.cvtColor(frame_np, cv2.COLOR_BGR2GRAY), black, white, cv2.THRESH_BINARY)

        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        frame_copy = cv2.cvtColor(frame_np, cv2.COLOR_RGB2BGR).copy()

        cv2.drawContours(frame_copy, contours, -1, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow("Result", frame_copy)

        cv2.imshow("Binary Test", thresh)
 

        key = cv2.waitKey(1)

        if key:
            if key == ord('n'):
                version =  0 if version + 1 > 4 else version + 1

            if key == 27:
                cv2.destroyAllWindows()
                break
    
    print("Done :)")
