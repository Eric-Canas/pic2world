from math import radians

class Camera:
    """
    This class implements all the camera parameters
    """
    def __init__(self, pixel_size_mm : float, focal_length_mm : float, angle_degrees : float):
        """
        Initialize the camera parameters
        """
        self.pixel_size_mm = pixel_size_mm
        self.pixel_size_cm = pixel_size_mm / 10.0
        self.pixel_size_m = pixel_size_mm / 1000.0
        self.focal_length_mm = focal_length_mm
        self.focal_length_cm = focal_length_mm / 10.0
        self.focal_length_m = focal_length_mm / 1000.0

        self.angle_degrees = angle_degrees
        self.angle_radians = radians(angle_degrees)

        self.lens_power_diopters = 1000.0 / self.focal_length_mm
        self.lens_power_mm = self.lens_power_diopters * 0.2645
