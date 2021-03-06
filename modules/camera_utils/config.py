from modules.camera_utils.camera import Camera
from math import sqrt

REDMI_NOTE_11_PRO_MAIN = 'Redmi Note 11 Pro - Main'
REDMI_NOTE_11_PRO_SELFIE = 'Redmi Note 11 Pro - Selfie'
CANON_EOS_R6 = 'Canon EOS R6'
REDMI_NOTE_11_PRO_MAIN_CAMERA = Camera( # Samsung ISOCELL HM2 1/1.52"
        pixel_size_mm=(0.7*sqrt(9)*4)/1000.0, # Uses Nona-Bayer (9 pixels combined). 108MP -> 12MP
        focal_length_mm=24,
        # aperture is f/1.9,
        sensor_shape_px=(4000, 3000),
    )
REDMI_NOTE_11_PRO_SELFIE_CAMERA = Camera( # OmniVision OV16A1Q 1/3.06"
            pixel_size_mm=1.0*sqrt(4)/1000.0, # Uses Quad-Bayer (4 pixels combined) 12MP. Otherwise 0.7um
            focal_length_mm=24, # I'm not sure. It just says wide
            # aperture is f/2.4,
    )
CANON_EOS_R6_CAMERA = Camera( # Canon EOS R6
        pixel_size_mm=8.18/1000.0, # Not totally sure. Assuming it is equivalent to Canon EOS 1D Mark II
        focal_length_mm=50, # The one I commonly use
        # aperture is f/1.4,
        sensor_shape_px=(5472, 3648)
    )
IPHONE_13_PRO_MAX_MAIN_CAMERA = Camera( # Apple iPhone 13 Pro Max - Main
        pixel_size_mm=1.9*sqrt(4)/1000.0,
        focal_length_mm=6,
        # aperture is f/1.5,
        sensor_shape_px=(4032, 3024),
    )

CAMERAS = {
    REDMI_NOTE_11_PRO_MAIN: REDMI_NOTE_11_PRO_MAIN_CAMERA,
    REDMI_NOTE_11_PRO_SELFIE: REDMI_NOTE_11_PRO_SELFIE_CAMERA,
    CANON_EOS_R6: CANON_EOS_R6_CAMERA
}