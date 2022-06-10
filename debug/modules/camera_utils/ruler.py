from modules.camera_utils.ruler import Ruler
from debug.constants import RULER_SAMPLE_IMAGE, IMAGES_PATH, FILE, CAMERA,\
                            DISTANCE_CM, ELEMENT_LENGTH_IN_PX, ELEMENT_HEIGHT_IN_CM

if __name__ == '__main__':
    #img = cv2.imread(os.path.join(IMAGES_PATH, RULER_SAMPLE_IMAGE[FILE]))
    # Get the camera
    camera = RULER_SAMPLE_IMAGE[CAMERA]
    ruler = Ruler(camera = camera)
    img_distance = ruler.distance_to_object(object_length_px=RULER_SAMPLE_IMAGE[ELEMENT_LENGTH_IN_PX],
                                        real_object_length_cm=RULER_SAMPLE_IMAGE[ELEMENT_HEIGHT_IN_CM])
    print("Distance to object: Calculated: {calc} cm - Real {real} cm".format(calc=img_distance,
                                                                              real=RULER_SAMPLE_IMAGE[DISTANCE_CM]))
    object_height = ruler.object_length_in_cm(object_length_px=RULER_SAMPLE_IMAGE[ELEMENT_LENGTH_IN_PX],
                                                distance_to_object_cm=RULER_SAMPLE_IMAGE[DISTANCE_CM])
    print("Object height: Calculated: {calc} cm - Real {real} cm".format(calc=object_height,
                                                                        real=RULER_SAMPLE_IMAGE[ELEMENT_HEIGHT_IN_CM]))