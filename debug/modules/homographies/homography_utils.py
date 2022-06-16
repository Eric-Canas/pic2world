import os
import cv2
from modules.homographies.homography_utils import *
from debug.constants import RULER_SAMPLE_IMGS, CAMERA, IMAGES_PATH,\
                            DISTANCE_CM, ELEMENT_LENGTH_IN_PX, ELEMENT_HEIGHT_IN_CM, DEGREES, FILE


if __name__ == '__main__':
    # Get the camera
    RULER_SAMPLE_IMGS = {'Canon EOS R6 - Horizontal - 60 deg' : RULER_SAMPLE_IMGS['Canon EOS R6 - Horizontal - 60 deg']}
    for sample, sample_params in RULER_SAMPLE_IMGS.items():
        print("For sample: {sample}".format(sample=sample))
        img_file = os.path.join(IMAGES_PATH, sample_params[FILE])
        img = cv2.imread(img_file)
        correct_polygon_perspective(img, origin_polygon=None, interactive=True)