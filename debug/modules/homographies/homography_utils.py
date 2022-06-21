import os
import cv2
import numpy as np

from modules.homographies.homography_utils import *
from debug.constants import RULER_SAMPLE_IMGS, IMAGES_PATH, DEGREES, FILE


if __name__ == '__main__':
    # Get the camera
    RULER_SAMPLE_IMGS = {'CANON EOS R6 - Pic2World' : RULER_SAMPLE_IMGS['CANON EOS R6 - Pic2World']}
    for sample, sample_params in RULER_SAMPLE_IMGS.items():
        print("For sample: {sample}".format(sample=sample))
        img_file = os.path.join(IMAGES_PATH, sample_params[FILE])
        img = cv2.imread(img_file)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        correct_polygon_perspective(img, origin_polygon=None, interactive=True, angle_degrees=sample_params[DEGREES],
                                    output_shape=(600, 300), pad = 0.05, verbose=True)