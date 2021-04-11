import cv2 as cv

import config
import pickle
import skimage.metrics


def roiFromPoints(image, point1, point2):
    x1, y1, x2, y2 = point1[0], point1[1], point2[0], point2[1]
    return(image[y1:y2, x1:x2])


class Detector:
    def __init__(self, id):
        self.id=id
        self.detect_last=False
        self.detect_count=0
        self.template=None
        self.w=0
        self.h=0
        self.load_template()

    def load_template(self):
        try:
            self.template=cv.imread(self.id+".png", cv.IMREAD_COLOR)
            self.point=pickle.load(open(self.id+".meta", "rb"))
        except Exception as e:
            print(e)
            return

        self.h, self.w, channels = self.template.shape

    def update_template(self, image, point1, point2):

        self.template=roiFromPoints(image, point1, point2)
        self.point=point1
        # cv.imshow('test', self.template)

        cv.imwrite(self.id+".png", self.template)
        pickle.dump(self.point, open(self.id+".meta", "wb"))

        self.h, self.w, channels = self.template.shape

    def analyse(self, input_frame, output_frame):

            if self.template is None:
                return None

            point2=( self.point[0] + self.w, self.point[1] + self.h )
            roi=roiFromPoints(input_frame, self.point, point2 )

            # cv.imshow("roi", roi)
            # cv.imshow("templ", self.template)

            match=skimage.metrics.structural_similarity(roi, self.template, multichannel=True)


            if match >= config.detect_threshold:
                detect=True
                color = (0, 255, 0)
            elif match <= config.undetect_threshold:
                detect=False
                color = (0, 0, 255)
            else:
                #consider it noise
                color=(128,128,128)
                detect=None

            #if we're detecting something (true/false), restart counting
            if detect is not None:
                if detect!=self.detect_last:
                    self.detect_last=detect
                    self.detect_count=0
                else:
                    self.detect_count=self.detect_count+1

            #now determie result
            txt=""
            if self.detect_count>=config.detect_frames:
                result=self.detect_last
                if result:
                    txt="DETECTED!"
            else:
                result=None

            #visual feedback
            thickness=2
            cv.rectangle(output_frame, self.point, point2, color, thickness)
            cv.putText(output_frame, "{} {:0.2f} {}".format(self.id, match, txt), self.point, cv.FONT_HERSHEY_SIMPLEX, 1, (255,255,255))

            return result

        # def analyse(self, input_frame, output_frame):
        #
        #     if self.template is not None:
        #         return None
        #
        #     res = cv.matchTemplate(input_frame, self.template, method=cv.TM_CCOEFF_NORMED)
        #     min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
        #     top_left = max_loc
        #     bottom_right = (top_left[0] + self.w, top_left[1] + self.h)
        #
        #     if max_val >= config.detect_threshold:
        #         detect = True
        #     elif max_val <= config.undetect_threshold:
        #         detect = False
        #     else:
        #         # consider it noise
        #         return None
        #
        #     if detect != self.detect_last:
        #         self.detect_last = detect
        #         self.detect_count = 0
        #     else:
        #         self.detect_count = self.detect_count + 1
        #
        #     # visual feedback of detection state
        #     if self.detect_count >= config.detect_frames:
        #         if detect:
        #             color = (0, 255, 0)
        #         else:
        #             color = (0, 0, 255)
        #     else:
        #         color = (128, 128, 128)
        #
        #     thickness = 2
        #
        #     cv.rectangle(output_frame, top_left, bottom_right, color, thickness)
        #     cv.putText(output_frame, "{}: {:0.2f}".format(self.id, max_val), top_left, cv.FONT_HERSHEY_SIMPLEX, 1,
        #                (255, 255, 255))
        #
        #     if self.detect_count >= config.detect_frames:
        #         return detect
        #     else:
        #         return None
        #