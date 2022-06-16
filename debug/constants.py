import os
from modules.camera_utils.config import REDMI_NOTE_11_PRO_MAIN_CAMERA, CANON_EOS_R6_CAMERA

CAMERA = "camera"
FILE = "file"
DISTANCE_CM = "distance_cm"
ELEMENT_HEIGHT_IN_CM = "element_height_in_cm"
ELEMENT_LENGTH_IN_PX = "element_height_in_px"
DEGREES = "degrees"
Y1 = "y1"

IMAGES_PATH = os.path.join(os.path.dirname(__file__), 'resources')

RULER_SAMPLE_IMGS = {
    'Redmi Note 11 Pro - Main - Vertical': {
        FILE: "dist-300-meter-150-angle-0-camera-canon-eos-R6.JPG",
        CAMERA: REDMI_NOTE_11_PRO_MAIN_CAMERA,
        DISTANCE_CM: 160, # Distance to the element to measure
        ELEMENT_HEIGHT_IN_CM: 160.0, # Distance
        ELEMENT_LENGTH_IN_PX: 2873, # Number of pixels
        Y1: 0,
        DEGREES: 0 # Angle of the element to measure
    },
    'Canon EOS R6 - Vertical': {
        FILE: "dist-300-meter-150-angle-0-camera-canon-eos-R6.JPG",
        CAMERA: CANON_EOS_R6_CAMERA,
        DISTANCE_CM: 300.0, # Distance to the element to measure
        ELEMENT_HEIGHT_IN_CM: 148.0, # Distance
        ELEMENT_LENGTH_IN_PX: 3178, # Number of pixels
        Y1: 0,
        DEGREES: 0 # Angle of the camera with respect to the element
    },
    'Canon EOS R6 - Horizontal - 90 deg': {
        FILE : 'dist-100-large-90-ange-90deg-canon-eos-r6.JPG',
        CAMERA: CANON_EOS_R6_CAMERA,
        DISTANCE_CM: 100.0, # Distance to the element to measure
        ELEMENT_HEIGHT_IN_CM: 90.0, # Distance
        ELEMENT_LENGTH_IN_PX: 146, # Number of pixels
        Y1: 1910, # Y1 coordinate of the element
        DEGREES: 90#89.8 # Angle of the camera with respect to the element
    },
    'Canon EOS R6 - Horizontal - 60 deg': {
        FILE : 'dist-118-large-90-ange-60deg-canon-eos-r6.JPG',
        CAMERA: CANON_EOS_R6_CAMERA,
        DISTANCE_CM: 118.0, # Distance to the element to measure
        ELEMENT_HEIGHT_IN_CM: 90.0, # Distance
        ELEMENT_LENGTH_IN_PX: 2320, # Number of pixels
        Y1: 1184,
        DEGREES: 60 # Angle of the camera with respect to the element
    }
}