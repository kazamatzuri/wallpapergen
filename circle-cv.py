import cv2  # Not actually necessary if you just want to create an image.
import numpy as np
from sand import Sand
import numpy.random import random

height,width=512,512
img = np.zeros((height,width,3), np.uint8)
img = cv2.line(img,(0,0),(511,511),(255,0,0),5)
img = cv2.circle(img,(447,63), 63, (0,0,255), -1)
cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite('test.png',img)