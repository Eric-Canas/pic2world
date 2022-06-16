"""
This file contains the class Ruler, which is used to calculate real-world distances
from image distances and the camera parameters. All these calculations are based
in the Thin-Lens Equation.
Author: Eric Canas
Mail: eric@ericcanas.com
GitHub: https://github.com/Eric-Canas
License: MIT
"""
from modules.camera_utils.camera import Camera
import math
import numpy as np

class Ruler:
    """
    This class functions are used to calculate the real-world distances from the image distances
    and the camera parameters. All these calculations are based in the Thin-Lens Equation.
    """

    def __init__(self, camera: Camera):
        """
        Initializes the ruler.
        """
        assert isinstance(camera, Camera), "The camera must be a Camera object"
        self.camera = camera

    def distance_to_object_cm(self, object_length_px: float, real_object_length_cm: float,
                              angle_degrees: int|float|None = 0,
                              object_y1_px: int | float = 0) -> float:
        """
        Given the number of pixels that an object occupies in the image and the real
        height of the element, estimates the distance from the camera lens to the object in cm.
        Uses the Gauss formula for lenses (thin-lens equation) and the camera parameters
        to calculate it.
        This function assumes no distortion in the image.
        Thin-lens equation -> (1/object_distance) + (1/image_distance) = 1/focal_length
        Other similarities -> real_size/size_in_sensor = focal_length/distance_to_object
        parameters:
            object_length_px: int | float: The number of pixels that an object occupies in the image.
            real_object_length_cm: float: The real height of the object in cm.
            angle_degrees: int|float|None: The angle between the camera and the plain of the object in
                                           which we are measuring the object length. If the object is
                                           standing in front of the camera (as usually), angle
                                           is 0. Use None if the angle is unknown. Default: 0.
            object_y1_px: int|float: The y coordinate of the top of the object in the image. It is only
                                     used when the angle is very close to 90º (perpendicular), so the field of view
                                     have a high impact on the measure. Default: 0.
        return:
            float: The distance from the camera lens to the object in cm.
        """
        # Get the pixel size in centimeters
        if angle_degrees is None:
            object_measure_in_sensor_cm = self.camera.px_to_cm(px=object_length_px)
        else:
            # Correct the perspective
            object_measure_in_sensor_cm = self.__correct_z_perspective(object_degrees=angle_degrees,
                                                                       object_y1_px=object_y1_px,
                                                                       object_y2_px=object_y1_px+object_length_px)
        magnification = real_object_length_cm / object_measure_in_sensor_cm
        distance_to_objective = self.camera.focal_length_cm * magnification
        return distance_to_objective

    def object_length_in_cm(self, distance_to_object_cm: float, object_length_px: float,
                            angle_degrees : None | float | int = 0,
                            object_y1_px: int | float = 0) -> float:
        """
        Given the distance from the camera lens to the object in cm and the number of pixels that
        an object occupies in the image, estimates the real height of the object in cm.
        Uses the Gauss formula for lenses (thin-lens equation) and the camera parameters
        to calculate it.
        This function assumes no distortion in the image.
        Thin-lens equation -> (1/object_distance) + (1/image_distance) = 1/focal_length
        Other similarities -> real_size/size_in_sensor = focal_length/distance_to_object
        parameters:
            distance_to_object_cm: float: The distance from the camera lens to the object in cm.
            object_length_px: int | float: The number of pixels that the object occupies in the image.
            angle_degrees: int|float|None: The angle between the camera and the plain of the object in
                                            which we are measuring the object length. If the object is
                                            standing in front of the camera (as usually), angle
                                            is 0. Use None (or 0) if the angle is unknown. Default: 0.
        return:
            float: The real height of the object in cm.
        """
        if angle_degrees is None:
            object_measure_in_sensor_cm = self.camera.px_to_cm(px=object_length_px)
        else:
            # Correct the perspective
            object_measure_in_sensor_cm = self.__correct_z_perspective(object_degrees=angle_degrees,
                                                                       object_y1_px=object_y1_px,
                                                                       object_y2_px=object_y1_px+object_length_px)
        # Calculate the magnification from the distances (real_distance/focal_length)
        magnification = distance_to_object_cm / self.camera.focal_length_cm
        real_object_length_cm = object_measure_in_sensor_cm * magnification
        return real_object_length_cm


    # ------------------------------ PRIVATES ---------------------------------

    def __correct_z_perspective(self, object_degrees: float | int, object_y1_px: float | int,
                                object_y2_px: float | int):
        """
        Given an object that occupies object_y1_px to object_y2_px pixels in the image,
        when it is with a perspective of object_degrees degrees, by a camera with a given
        lens aperture, return the object_y1_px to object_y2_px that would correspond if
        it was seen at 0 degrees.
        """
        assert object_y1_px <= object_y2_px, "object_y1_px must be smaller than object_y2_px"
        assert self.camera.sensor_shape_px is not None, "camera.sensor_shape_px must be known to correct perspective"

        object_perspective_radians = math.radians(object_degrees)
        object_length_px = object_y2_px - object_y1_px
        # Get the object length in centimeters
        object_length_cm = self.camera.px_to_cm(px=object_length_px)
        # Count the amount of pixels over the top half of the camera sensor
        object_field_of_view = 0.0
        if abs(90 - object_degrees) < 5:
            object_field_of_view = self.__calculate_field_of_view_affectation(object_y1_px, object_y2_px)
        # Get the object length in cm with the perspective corrected
        object_length_cm_perspective_corrected = object_length_cm / np.cos(
            object_perspective_radians - object_field_of_view)
        # Object perspective coming from 33 degrees and sin works
        return object_length_cm_perspective_corrected

    def __calculate_field_of_view_affectation(self, object_y1_px: int | float, object_y2_px: int | float):
        sensor_half_height_px = self.camera.sensor_shape_px[0] / 2
        top_half_px = min(sensor_half_height_px, object_y2_px) - min(object_y1_px, sensor_half_height_px)
        bottom_half_px = max(sensor_half_height_px, object_y2_px) - max(object_y1_px, sensor_half_height_px)
        percentage_of_sensor = abs(top_half_px - bottom_half_px) / self.camera.sensor_shape_px[0]
        # Let's assume that field of view only affects when the angle is very hard
        object_field_of_view = self.camera.sensor_aperture_radians[0] * percentage_of_sensor
        return object_field_of_view