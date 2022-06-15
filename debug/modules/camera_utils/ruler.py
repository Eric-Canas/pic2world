from modules.camera_utils.ruler import Ruler
from debug.constants import RULER_SAMPLE_IMGS, CAMERA,\
                            DISTANCE_CM, ELEMENT_LENGTH_IN_PX, ELEMENT_HEIGHT_IN_CM, DEGREES, Y1

if __name__ == '__main__':
    #img = cv2.imread(os.path.join(IMAGES_PATH, RULER_SAMPLE_IMAGE[FILE]))
    # Get the camera
    for sample, sample_params in RULER_SAMPLE_IMGS.items():
        print("For sample: {sample}".format(sample=sample))
        camera = sample_params[CAMERA]
        ruler = Ruler(camera = camera)
        img_distance = ruler.distance_to_object_cm(object_length_px=sample_params[ELEMENT_LENGTH_IN_PX],
                                                   real_object_length_cm=sample_params[ELEMENT_HEIGHT_IN_CM],
                                                   angle_degrees=sample_params[DEGREES],
                                                   object_y1_px=sample_params[Y1])
        print("\tDistance to object: Calculated: {calc} cm - Real {real} cm".format(calc=img_distance,
                                                                                  real=sample_params[DISTANCE_CM]))
        object_height = ruler.object_length_in_cm(object_length_px=sample_params[ELEMENT_LENGTH_IN_PX],
                                                  distance_to_object_cm=sample_params[DISTANCE_CM],
                                                  angle_degrees=sample_params[DEGREES],
                                                  object_y1_px=sample_params[Y1])
        print("\tObject height: Calculated: {calc} cm - Real {real} cm".format(calc=object_height,
                                                                            real=sample_params[ELEMENT_HEIGHT_IN_CM]))