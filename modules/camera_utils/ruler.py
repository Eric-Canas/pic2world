import numpy as np
from modules.camera_utils.camera import Camera
from modules.camera_utils.homography import *


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

    def distance_to_object(self, object_length_px: float, real_object_length_cm: float,
                           angle_degrees = 90, object_y1_px: int | float = 0) -> float:
        """
        Given the number of pixels that an object occupies in the image and the real
        height of the element, return the distance (in z) to the object in cm.
        Uses the Gauss formula for lenses (thin-lens equation) and the camera parameters
        to calculate it.
        This function assumes no distortion in the image.
        Thin-lens equation: (1/object_distance) + (1/image_distance) = 1/focal_length
        Other similarities: real_size/size_in_sensor = focal_length/distance_to_object
        object_length_px: the number of pixels that an object occupies in the image
        real_object_length_cm: the real height of the element in cm
        return: the distance to the object in cm
        """
        # Get the pixel size in centimeters
        if angle_degrees is None:
            object_measure_in_sensor_cm = self.camera.px_to_cm(px=object_length_px)
        else:
            # Correct the perspective
            object_measure_in_sensor_cm = correct_z_perspective(camera=self.camera,
                                                                object_degrees=angle_degrees,
                                                                object_y1_px=object_y1_px,
                                                                object_y2_px=object_y1_px+object_length_px)
        #object_measure_in_sensor_cm = self.camera.px_to_cm(px=object_length_px)
        magnification = real_object_length_cm / object_measure_in_sensor_cm
        distance_to_objective = self.camera.focal_length_cm * magnification
        return distance_to_objective

    def object_length_in_cm(self, distance_to_object_cm: float, object_length_px: float,
                            angle_degrees : None | float | int = None,
                            object_y1_px: int | float = 0) -> float:
        """
        Given the distance to the object in cm and the number of pixels that the object
        occupies in the image, return the real height of the object in cm.
        distance_to_object_cm: the distance to the object in cm
        object_length_px: the number of pixels that an object occupies in the image
        return: the real height of the object in cm
        """
        if angle_degrees is None:
            object_measure_in_sensor_cm = self.camera.px_to_cm(px=object_length_px)
        else:
            # Correct the perspective
            object_measure_in_sensor_cm = correct_z_perspective(camera=self.camera,
                                                                object_degrees=angle_degrees,
                                                                object_y1_px=object_y1_px,
                                                                object_y2_px=object_y1_px+object_length_px)
        # Calculate the magnification from the distances (real_distance/focal_length)
        magnification = distance_to_object_cm / self.camera.focal_length_cm
        real_object_length_cm = object_measure_in_sensor_cm * magnification
        return real_object_length_cm