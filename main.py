# import numpy as np
import cv2
# from matplotlib import pyplot as plt


import config


from Detector import Detector
from MouseSelector import MouseSelector



############# prepare opencv

cap = cv2.VideoCapture(config.v4l_device)
cap.set(cv2.CAP_PROP_FPS,2)
print(cap.get(cv2.CAP_PROP_FPS))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.height)

cv2.namedWindow('frame', cv2.WINDOW_NORMAL)

skip_detector = Detector(id="skip_button")
ads_detector = Detector(id="ads_logo")
selector= MouseSelector("frame")

######################### mainloop
ads_active=False
skipped=False
show=False
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    key=cv2.waitKey(1)

    #quit
    if key & 0xFF == ord('q'):
        break

    #set skip image
    if key & 0xFF == ord('s'):
        skip_detector.update_template(frame, selector.point1, selector.point2)

    if key & 0xFF == ord('a'):
        ads_detector.update_template(frame, selector.point1, selector.point2)

    selector.draw(frame)

    if not ret:
        continue

    ads_detected=ads_detector.analyse(frame, frame)
    if ads_detected==True:
        if not ads_active:
            ads_active=True
            config.controller.notify("Ad detected")
            print("Ads detected, pressing mute")
            config.controller.mute()
    elif ads_detected==False:
        if ads_active:
            print("No more ads detected, pressing unmute")
            ads_active=False
            config.controller.unmute()
    else:
        #changing...
        pass

    skip_detected=skip_detector.analyse(frame, frame)
    if skip_detected==True:
        if not skipped:
            print("Skip button detected, pressing skip")
            skipped = True
            config.controller.skip()
    elif skip_detected==False:
        skipped=False

    show = not show
    # if show:
    cv2.imshow('frame',frame)


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
