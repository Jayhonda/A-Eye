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
    hwnd = win.FindWindow(None, "Untitled - Paint")

    # Store window dimension
    dimensions = win.GetWindowRect(hwnd)

    # Capture the frame
    image = ImageGrab.grab(dimensions)

    # Convert image into NP Array
    image_np = np.array(image)

    if version == 0:
        # Display in full colors
        return cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    elif version == 1:
        # Display in grayscale
        return cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
    else:
        # Displays all the outlines
        return cv2.Canny(image_np, 100, 100)
    

if __name__ == "__main__":
    print("Running...")
    
    version = 0
    
    while True:
        frame = screen_grab(version)

        cv2.imshow("Analyze Screen", frame)

        if cv2.waitKey(1) & 0xFF == ord('n'):
            version =  0 if version + 1 > 3 else version + 1

        if cv2.waitKey(1) & 0xFF == 27:
            cv2.destroyAllWindows()
            break
    print("Done :)")
