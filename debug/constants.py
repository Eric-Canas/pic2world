import os
from modules.camera_utils.config import REDMI_NOTE_11_PRO_MAIN_CAMERA, CANON_EOS_R6_CAMERA

CAMERA = "camera"
FILE = "file"
DISTANCE_CM = "distance_cm"
ELEMENT_HEIGHT_IN_CM = "element_height_in_cm"
ELEMENT_LENGTH_IN_PX = "element_height_in_px"

IMAGES_PATH = os.path.join(os.path.dirname(__file__), 'resources')
RULER_SAMPLE_IMAGE = {
    FILE: "dist-300-meter-150-angle-0-camera-canon-eos-R6.JPG",
    CAMERA: CANON_EOS_R6_CAMERA,
    DISTANCE_CM: 300.0, # Distance to the element to measure
    ELEMENT_HEIGHT_IN_CM: 150.0, # Distance
    ELEMENT_LENGTH_IN_PX: 3179 # Number of pixels


}