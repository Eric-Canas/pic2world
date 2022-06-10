from math import radians, atan, cos

class Camera:
    """
    This class implements all the camera parameters
    """
    def __init__(self, pixel_size_mm: float, focal_length_mm: float, sensor_shape_px: tuple[int, int] | None = None,
                 angle_degrees: float = 0.0):
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

        self.sensor_shape_px = sensor_shape_px

        if sensor_shape_px is not None:
            assert len(sensor_shape_px) == 2, "The sensor shape must be a tuple of two integers"
            self.sensor_shape_mm = tuple(x * self.pixel_size_mm for x in sensor_shape_px)
            self.sensor_shape_cm = tuple(x * self.pixel_size_cm for x in sensor_shape_px)
            self.sensor_shape_m = tuple(x * self.pixel_size_m for x in sensor_shape_px)

            self.sensor_aperture_degrees = tuple(2 * atan(x / (2 * self.focal_length_cm)) for x in self.sensor_shape_cm)
            self.cos_of_half_aperture_width = tuple(cos(radians(aperture / 2.0)) for aperture in self.sensor_aperture_degrees)
        else:
            self.sensor_shape_mm, self.sensor_shape_cm, self.sensor_shape_m = None, None, None
            self.sensor_aperture_degrees, self.cos_of_half_aperture_width = None, None
