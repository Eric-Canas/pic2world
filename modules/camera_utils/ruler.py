import numpy as np
import cv2
from modules.camera_utils.camera import Camera


class Ruler:
    """
    This class implements the utils for, given a camera, transform pixel measures into
    real world distances
    """

    def __init__(self, camera: Camera):
        """
        Initialize the ruler
        """
        self.camera = camera

    def pixel_to_distance_cm(self, pixel_measure: float, distance_to_object_cm: float) -> float:
        """
        Given a pixel measure (height or width), return the corresponding large in cm.
        Uses the Gauss formula for lenses (thin-lens equation) and the camera parameters
        to calculate it.
        Thin-lens equation: (1/object_distance) + (1/image_distance) = 1/focal_length
        Other similarities: size_in_img_h1/pixel_measure_h0 = focal_length/distance_to_object
        pixel_measure: the measure in pixels to measure
        distance_to_object_cm: the from the lens to the object (z axis) in cm
        """
        # Get the pixel size in centimeters
        object_measure_cm = pixel_measure * self.camera.pixel_size_cm
        # Get the angle in radians
        angle_radians = np.deg2rad(self.camera.angle_degrees)
        # Get the object length in centimeters (width or height)
        object_length_cm = distance_to_object_cm / \
                           (self.camera.focal_length_cm * object_measure_cm * np.tan(angle_radians))
        return object_length_cm