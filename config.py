
# v4l device, e.g. /dev/video0 is 0
v4l_device=4
width=1920
height=1080

#number of frames before we can be sure something is detected
detect_frames=5
undetect_threshold=0.33
detect_threshold=0.66

# tv controller
import  ControlWebos
controller=ControlWebos.ControlWebos()
