import numpy as np
from modules.interactive.interactive_plots import draw_polygon_by_clicking
from warnings import warn
from modules.camera_utils.camera import Camera


def correct_polygon_perspective(img: np.ndarray,
                                origin_polygon: tuple[tuple[int|float, int|float], tuple[int|float, int|float],
                                                tuple[int|float, int|float], tuple[int|float, int|float]] | np.ndarray |
                                                None,
                                angle_degrees: int|float|None = 0,
                                camera: Camera | None = None,
                                interactive: bool = True,
                                verbose: bool = True) -> np.ndarray:
    # Consistency Checks
    assert type(camera) in {Camera, type(None)}, "camera must be a Camera object"
    if type(img) is np.ndarray:
        assert img.ndim == 3 or img.ndim == 2, "Image must be a 2D or 3D array"
    if origin_polygon is not None:
        assert type(origin_polygon) in {tuple, list, np.ndarray} and all(len(coords) == 2 for coords in origin_polygon),\
            "origin_polygon must have 4 coordinates"
        if interactive:
            warn("Interactive mode overrides origin_polygon, it will not be used", UserWarning)
    else:
        assert interactive, "Interactive mode is required if origin_polygon is not given"
    assert (type(angle_degrees) in {type(None), int, float, np.float32, np.int32, np.float64, np.int64}), \
        f"Angle_degrees must be a number or None. Got {type(angle_degrees)}"

    # Definition of the polygon
    if interactive:
        corners = draw_polygon_by_clicking(img=img, sides=4, verbose=verbose)
        if corners is None:
            if origin_polygon is not None:
                warn("Interactive polygon definition aborted, using origin_polygon", UserWarning)
            else:
                raise ValueError("Interactive polygon definition aborted")
        else:
            origin_polygon = corners
            if verbose:
                print("Polygon Definition: {corners}".format(corners=corners))
    # Homography
    return img
