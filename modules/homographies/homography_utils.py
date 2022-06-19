import numpy as np
from modules.interactive.interactive_plots import draw_polygon_by_clicking
from modules.geometry.geometry_utils import circumscribed_rectangle, get_polygon_shape, center_polygon
from warnings import warn
from modules.camera_utils.camera import Camera
import cv2
from matplotlib import pyplot as plt

def correct_polygon_perspective(img: np.ndarray,
                                origin_polygon: tuple[tuple[int|float, int|float], tuple[int|float, int|float],
                                                tuple[int|float, int|float], tuple[int|float, int|float]] | np.ndarray |
                                                None,
                                output_shape : tuple[int, int] | list[int, int] | np.ndarray | None = None,
                                angle_degrees: int|float|None = None,
                                camera: Camera | None = None,
                                interactive: bool = False,
                                verbose: bool = False) -> np.ndarray:
    """
    Corrects the perspective of an image to make a given polygon looks like a rectangle.
    If origin_polygon is None, interactive should be True, so the user will be asked to set a valid one.
    Args:
        img: Numpy array of shape (height, width, channels) or (height, width). The image to correct.
        origin_polygon: Tuple of shape (4, 2). The polygon to use as a reference. If not given,
                    interactive should be True, so the user will be asked to draw a polygon. If both it is given,
                    and interactive is True, user will be asked anyway and it will be used as a fallback.
        output_shape: Tuple of shape (height, width). The shape of the output image. If not given, the output
                     shape will be the same as the output rectangle, and it will be isolated in the image. If given,
                     the output rectangle will be resized and placed in the center of the image.
        angle_degrees: Float, Integer or None. Angle of the camera with which the image was taken.
                        If known, it will be used to infer the aspect ratio of the output image. Default is None.
        camera: Camera object. If given, it will be used to infer the aspect ratio of the output rectangle together with
                the angle.
        interactive: Boolean. If True, the user will be asked to draw a polygon, in that case, origin_polygon
                    can be None. If both Interactive is True and origin_polygon is not None, that origin_polygon
                    will be used as a fallback. Default is False.
        verbose: Boolean. If True, verbose the process. Default is False.
    Returns:
        Numpy array of shape (out_height, out_width, channels) or (out_height, out_width). The corrected image.
    """
    # Consistency Checks
    assert type(camera) in {Camera, type(None)}, "camera must be a Camera object"
    if type(img) is np.ndarray:
        assert img.ndim == 3 or img.ndim == 2, "Image must be a 2D or 3D array"
    if origin_polygon is not None:
        assert type(origin_polygon) in {tuple, list, np.ndarray} and all(len(coords) == 2 for coords in origin_polygon) \
               and len(origin_polygon) == 4, "origin_polygon must have 4 coordinates"
    else:
        assert interactive, "Interactive mode is required if origin_polygon is not given"
    assert (type(angle_degrees) in {type(None), int, float, np.float32, np.int32, np.float64, np.int64}), \
        f"Angle_degrees must be a number or None. Got {type(angle_degrees)}"

    # Definition of the polygon
    if interactive:
        origin_polygon = draw_polygon_by_clicking(img=img, sides=4, fallback_polygon=origin_polygon, verbose=verbose)
    # Compute the output polygon
    output_polygon = __compute_output_polygon(origin_polygon=origin_polygon, angle_degrees=angle_degrees, camera=camera,
                                              verbose=verbose)
    if output_shape is None:
        # Compute the polygon shape
        output_shape = get_polygon_shape(polygon=output_polygon, as_int=True)
    else:
        # Place the output polygon in the center of the image
        output_polygon = center_polygon(polygon=output_polygon, output_shape=output_shape)
    # Transform it to a numpy array
    origin_polygon, output_polygon = np.array(origin_polygon, dtype=np.float32), np.array(output_polygon, dtype=np.float32)
    H_matrix = cv2.getPerspectiveTransform(src=origin_polygon, dst=output_polygon)
    img = cv2.warpPerspective(src=img, M=H_matrix, dsize=output_shape)
    if verbose:
        plt.clf()
        plt.imshow(img)
        plt.show()
    return img

def __compute_output_polygon(origin_polygon: tuple[tuple[int|float, int|float], tuple[int|float, int|float],
                                                tuple[int|float, int|float], tuple[int|float, int|float]] | np.ndarray,
                             start_at_0_coord: bool = True,
                             angle_degrees: int|float|None = None, camera: Camera = None,
                             verbose: bool = False) -> tuple[tuple[int|float, int|float], ...] | np.ndarray:
    """
    Computes the output polygon given an origin_polygon.
    Args:
        origin_polygon: Tuple of shape (sides, 2). The polygon to use as a reference.
        start_at_0_coord: Boolean. If True, the output polygon will start at (0, 0). If False, it will use the
                             origin_polygon coordinates. Default is True.
        angle_degrees: Float, Integer or None. Angle of the camera with which the image was taken.
                        If known, it will be used to infer the aspect ratio of the output image. Default is None.
        camera: Camera object. If given, it will be used to infer the aspect ratio of the output rectangle together with
                the angle.
        verbose: Boolean. If True, verbose the process. Default is False.
    Returns:
        Tuple of shape (4, 2). The output polygon coordinates in the form ((x1, y1), (x2, y2), (x3, y3), (x4, y4)).
    """
    assert type(origin_polygon) in {tuple, list, np.ndarray} and all(len(coords) == 2 for coords in origin_polygon),\
        "origin_polygon must have 4 coordinates"
    assert type(angle_degrees) in {type(None), int, float, np.float32, np.int32, np.float64, np.int64}, \
        f"Angle_degrees must be a number or None. Got {type(angle_degrees)}"
    assert type(camera) in {type(None), Camera}, "camera must be a Camera object"
    assert type(verbose) is bool, "verbose must be a boolean"
    assert type(start_at_0_coord) is bool, "start_at_0_coord must be a boolean"

    # If angle is not given, assume that it is not relevant, so just output a rectangle circumscribing the polygon
    if angle_degrees is None:
        # Calculate the circumscribed rectangle
        return circumscribed_rectangle(polygon=origin_polygon, shift_to_coord=0. if start_at_0_coord else None)
    else:
        raise NotImplementedError("Not implemented yet")
