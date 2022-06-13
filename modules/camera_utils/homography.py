import math
from modules.camera_utils.camera import Camera
import cv2
import numpy as np

def correct_z_perspective(camera : Camera, object_degrees : float | int, object_y1_px : float | int,
                          object_y2_px : float | int):
    """
    Given an object that occupies object_y1_px to object_y2_px pixels in the image,
    when it is with a perspective of object_degrees degrees, by a camera with a given
    lens aperture, return the object_y1_px to object_y2_px that would correspond if
    it was seen at 0 degrees.
    """
    assert object_y1_px <= object_y2_px, "object_y1_px must be smaller than object_y2_px"
    assert camera.sensor_shape_px is not None, "camera.sensor_shape_px must be known to correct perspective"

    object_perspective_radians = math.radians(object_degrees)
    object_length_px = object_y2_px - object_y1_px
    # Get the object length in centimeters
    object_length_cm = camera.px_to_cm(px=object_length_px)
    # Count the amount of pixels over the top half of the camera sensor
    object_field_of_view = 0.0
    if abs(90 - object_degrees) < 5:
        object_field_of_view = calculate_field_of_view_affectation(camera, object_y1_px, object_y2_px)
    # Get the object length in cm with the perspective corrected
    object_length_cm_perspective_corrected = object_length_cm / np.cos(object_perspective_radians - object_field_of_view )
    # Object perspective coming from 33 degrees and sin works
    return object_length_cm_perspective_corrected


def calculate_field_of_view_affectation(camera : Camera, object_y1_px : int | float, object_y2_px : int | float):
    sensor_half_height_px = camera.sensor_shape_px[0] / 2
    top_half_px = min(sensor_half_height_px, object_y2_px) - min(object_y1_px, sensor_half_height_px)
    bottom_half_px = max(sensor_half_height_px, object_y2_px) - max(object_y1_px, sensor_half_height_px)
    percentage_of_sensor = abs(top_half_px - bottom_half_px) / camera.sensor_shape_px[0]
    # Let's assume that field of view only affects when the angle is very hard
    object_field_of_view = camera.sensor_aperture_radians[0] * percentage_of_sensor
    return object_field_of_view


def perspective(img, z_rotate):
    h = cv2.getRotationMatrix2D((img.shape[1]/2, img.shape[0]/2), z_rotate, 1)
    img = cv2.warpAffine(img, h, (img.shape[1], img.shape[0]))

    return img