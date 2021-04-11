import cv2
import cv2 as cv


class MouseSelector:
    def __init__(self, window_name):
        cv2.setMouseCallback(window_name, self.mouse_event)
        self.selecting=False
        self.point1=(0,0)
        self.point2=(0,0)

    def draw(self,img):
        cv2.rectangle(img, self.point1, self.point2, (255, 255, 255), 1)

    def mouse_event(self, event,x,y,flags,param):
        if event == cv.EVENT_LBUTTONDOWN:
            self.selecting=True
            self.point1=( x,y )
            self.point2=( x,y )
        elif event == cv.EVENT_MOUSEMOVE:
            if self.selecting:
                self.point2 = (x,y)
        elif event == cv.EVENT_LBUTTONUP:
            if self.selecting:
                self.point2 = (x,y)
                self.selecting=False

                #always make sure point1 is upper left and point2 lower right
                tmp=( min( self.point1[0], self.point2[0] ), min(self.point1[1], self.point2[1]))
                self.point2=( max( self.point1[0], self.point2[0] ), max(self.point1[1], self.point2[1]))
                self.point1=tmp

                print(self.point1, self.point2)