from math import radians, atan, cos

class Camera:
    """
    This class implements all the camera parameters
    """
    def __init__(self, pixel_size_mm: float, focal_length_mm: float,
                 sensor_shape_px: tuple[int|float, int|float] | None = None,
                 angle_degrees: float = 0.0):
        """
        Initialize the camera parameters
        """
        assert pixel_size_mm > 0.0, "The pixel size must be greater than 0"
        assert focal_length_mm > 0.0, "The focal length must be greater than 0"

        self.pixel_size_mm = pixel_size_mm
        self.pixel_size_cm = pixel_size_mm / 10.0
        self.pixel_size_m = pixel_size_mm / 1000.0
        self.focal_length_mm = focal_length_mm
        self.focal_length_cm = focal_length_mm / 10.0
        self.focal_length_m = focal_length_mm / 1000.0

        self.angle_degrees = angle_degrees
        self.angle_radians = radians(angle_degrees)

        self.lens_power_diopters = 1000.0 / self.focal_length_mm

        self.sensor_shape_px = sensor_shape_px

        if sensor_shape_px is not None:
            assert len(sensor_shape_px) == 2, "The sensor shape must be a tuple of two integers"
            self.sensor_shape_mm = tuple(x * self.pixel_size_mm for x in sensor_shape_px)
            self.sensor_shape_cm = tuple(x/10.0 for x in self.sensor_shape_mm)
            self.sensor_shape_m = tuple(x/1000.0 for x in self.sensor_shape_mm)

            self.sensor_aperture_radians = tuple(2 * atan(x / (2 * self.focal_length_mm)) for x in self.sensor_shape_mm)
            self.cos_of_half_aperture_width = tuple(cos(aperture / 2.0) for aperture in self.sensor_aperture_radians)
        else:
            self.sensor_shape_mm, self.sensor_shape_cm, self.sensor_shape_m = None, None, None
            self.sensor_aperture_radians, self.cos_of_half_aperture_width = None, None

    def px_to_mm(self, px: int | float) -> float:
        """
        Convert a number of pixels to the physical millimeters occupied in the sensor
        """
        return px * self.pixel_size_mm

    def px_to_cm(self, px: int | float) -> float:
        """
        Convert a number of pixels to the physical centimeters occupied in the sensor
        """
        return self.px_to_mm(px) / 10.0

    def px_to_m(self, px: int | float) -> float:
        """
        Convert a number of pixels to the physical meters occupied in the sensor
        """
        return self.px_to_mm(px) / 1000.0

