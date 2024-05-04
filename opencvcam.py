from maix import camera, display, image

import cv2
print(cv2)

img = image.new(size=(120, 120), mode="RGB", color=(255, 255, 255))
img.draw_line(0, 0, 120, 120)
img.draw_rectangle(40, 80, 120, 120, color=(255, 0, 0), thickness=16) #
img.draw_circle(120, 120, 20, color=(0, 255, 0))
img.draw_string(40, 40, "dalaoshu", 2, color=(0, 0, 255))

import cv2
import numpy as np
cv_img = cv2.imdecode(np.frombuffer(img.tobytes('jpg'), np.uint8), cv2.IMREAD_COLOR)

cv_img = cv_img[ : , : , (2,1,0)]

tmp = image.load(cv_img.tobytes(), cv_img.shape)

while True:
    img = camera.capture()    
    img.draw_image(tmp)
    display.show(img)         
