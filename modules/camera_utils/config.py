from modules.camera_utils.camera import Camera
from math import sqrt

REDMI_NOTE_11_PRO_MAIN = 'Redmi Note 11 Pro - Main'
REDMI_NOTE_11_PRO_SELFIE = 'Redmi Note 11 Pro - Selfie'
CANON_EOS_R6 = 'Canon EOS R6'

CAMERAS = {
    REDMI_NOTE_11_PRO_MAIN: Camera( # Samsung ISOCELL HM2 1/1.52"
        pixel_size_mm=(0.7*sqrt(9))/1000.0, # Uses Nona-Bayer (9 pixels combined). 108MP -> 12MP
        focal_length_mm=24,
        # aperture is f/1.9,
        angle_degrees=0.0 # Let's assume zenith angle
    ),
    REDMI_NOTE_11_PRO_SELFIE: Camera( # OmniVision OV16A1Q 1/3.06"
            pixel_size_mm=1.0*sqrt(4)/1000.0, # Uses Quad-Bayer (4 pixels combined) 12MP. Otherwise 0.7um
            focal_length_mm=24, # I'm not sure. It just says wide
            # aperture is f/2.4,
            angle_degrees=0.0 # Let's assume zenith angle
    ),
    CANON_EOS_R6: Camera( # Canon EOS R6
        pixel_size_mm=8.18/1000.0, # Not totally sure. Assuming it is equivalent to Canon EOS 1D Mark II
        focal_length_mm=50, # The one I commonly use
        # aperture is f/1.4,
        angle_degrees=0.0 # Let's assume zenith angle
    ),
}