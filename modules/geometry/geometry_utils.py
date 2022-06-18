"""
This module implements a few convenience functions for working with geometric shapes.
Author: Eric Canas
Mail: eric@ericcanas.com
GitHub: https://github.com/Eric-Canas
License: MIT
"""

import numpy as np

def order_2d_corners_clockwise(corners : np.ndarray | tuple[tuple[int | float, int | float], ...] |
                                         list[list[int | float, int | float], ...]) -> np.ndarray:
    """
    Order the corners of a polygon clockwise. Useful if you want to draw the polygon on an image.
    Args:
        corners: Iterable of 2D coordinates. The corners of the polygon in the form ((x1, y1), (x2, y2), ...).
    Returns:
        np.ndarray with the corners of the polygon in the form ((x1, y1), (x2, y2), ...), ordered clockwise.
    """
    assert type(corners) in {np.ndarray, tuple, list}, "The corners must be a numpy array, tuple or list"
    assert all(len(coords) == 2 for coords in corners), "The corners must be 2D coordinates"
    if type(corners) is not np.ndarray:
        corners = np.array(corners, dtype=np.float32)
    # Find the center of the rectangle
    center = np.mean(corners, axis=0)
    # Find the angle of each corner
    angles = np.arctan2(corners[:, 1]-center[1], corners[:, 0]-center[0])
    # Order the corners clockwise
    return corners[np.argsort(angles)]

def circumscribed_rectangle(polygon : np.ndarray | tuple[tuple[int | float, int | float], ...] |
                                      list[list[int | float, int | float], ...],
                            shift_to_coord_0: bool = False) -> tuple[tuple[int | float, int | float], ...]:
    """
    Compute the rectangle that circumscribes the given polygon.
    Args:
         polygon: Iterable of 2D coordinates. The corners of the polygon in the form ((x1, y1), (x2, y2), ...).
            shift_to_coord_0: If True, the coordinates of the rectangle will be shifted to start at (0, 0).
    Returns:
        Tuple of 4 2D coordinates or numpy array. The corners of the circumscribed rectangle in the form ((x1, y1), (x2, y2),
        (x3, y3), (x4, y4)). Given as tuple if polygon is a tuple or list, or numpy array if polygon is a numpy array.
    """
    assert type(polygon) in {np.ndarray, tuple, list}, "The corners must be a numpy array, tuple or list"
    assert all(len(coords) == 2 for coords in polygon), "The corners must be 2D coordinates"
    assert len(polygon) >= 2, "The polygon must have at least 2 corners"
    assert type(shift_to_coord_0) is bool, "The shift_to_coord_0 must be a boolean"

    x_min, x_max, y_min, y_max = get_x_y_min_max(polygon=polygon)
    if shift_to_coord_0:
        x_min, x_max, y_min, y_max = 0, x_max-x_min, 0, y_max-y_min
    return bbox_to_polygon((x_min, y_min, x_max, y_max))

def bbox_to_polygon(bbox : tuple[int | float, int | float, int | float, int | float] |
                           list[int | float, int | float, int | float, int | float] |
                           np.ndarray)\
        -> tuple[tuple[int | float, int | float], ...] | np.ndarray:
    """
    Convert a bounding box in the form (x1, y1, x2, y2) to a polygon in the form ((x1, y1), (x2, y2),
     (x3, y3), (x4, y4)).
    Args:
        bbox: Iterable of 4 integers or floats. The bounding box in the form (x1, y1, x2, y2).
    Returns:
        Tuple of 4 2D coordinates or numpy array. The corners of the bounding box in the form ((x1, y1), (x2, y2),
        (x3, y3), (x4, y4)) in format of tuple if bbox is a tuple or list, or numpy array if bbox is a numpy array.
    """
    assert len(bbox) == 4, "The bounding box must be a 4-tuple"
    polygon = ((bbox[0], bbox[2]), (bbox[1], bbox[2]), (bbox[1], bbox[3]), (bbox[0], bbox[3]))
    return polygon
def get_polygon_shape(polygon : np.ndarray | tuple[tuple[int | float, int | float], ...] |
                                 list[list[int | float, int | float], ...],
                      as_int: bool = False) -> tuple[int | float, int | float] | np.ndarray:
    """
    Compute the shape of the given polygon.
    Args:
         polygon: Iterable of 2D coordinates. The corners of the polygon in the form ((x1, y1), (x2, y2), ...).
         as_int: Boolean. If True, the shape will be returned as integers.
    Returns:
        Tuple of 2 integers or float. The width and height of the polygon.
    """
    x_min, x_max, y_min, y_max = get_x_y_min_max(polygon=polygon)
    if as_int:
        return (int(x_max-x_min), int(y_max-y_min))
    else:
        return (x_max-x_min, y_max-y_min)

def get_x_y_min_max(polygon : np.ndarray | tuple[tuple[int | float, int | float], ...] |
                                 list[list[int | float, int | float], ...]) -> tuple[int | float, int | float, int | float, int | float]:
    """
    Compute the minimum and maximum x and y coordinates of the given polygon.
    Args:
         polygon: Iterable of 2D coordinates. The corners of the polygon in the form ((x1, y1), (x2, y2), ...).
    Returns:
        4-tuple of integers. The minimum and maximum x and y coordinates of the polygon. In the form (x_min, x_max,
        y_min, y_max).
    """
    assert type(polygon) in {np.ndarray, tuple, list}, f"The corners must be a numpy array, tuple or list. Got {type(polygon)}"
    assert all(len(coords) == 2 for coords in polygon), "The corners must be 2D coordinates"
    assert len(polygon) >= 2, "The polygon must have at least 2 corners"

    x_min, x_max, y_min, y_max = float('inf'), -float('inf'), float('inf'), -float('inf')
    for x, y in polygon:
        x_min, x_max, y_min, y_max = min(x_min, x), max(x_max, x), min(y_min, y), max(y_max, y)
    return (x_min, x_max, y_min, y_max)

def center_polygon(polygon: np.ndarray | tuple[tuple[int | float, int | float], ...] |
                   list[list[int | float, int | float], ...],
                   output_shape: np.ndarray | tuple[int | float, int | float] |
                                 list[int | float, int |float],
                   resize_on_bigger: bool = True,
                   resize_on_lower: bool = False,
                   resize_pad: float = 0.05) -> tuple[tuple[int | float, int | float], ...]:
    """
    Center the coordinates of the polygon in the given shape.
    Args:
            polygon: Iterable of 2D coordinates. The corners of the polygon in the form ((x1, y1), (x2, y2), ...).
            output_shape: Tuple of 2 integers or float. The shape of the output element, in the form (width, height).
                            The polygon will be shifted to be placed in the center of this shape.
            resize_on_bigger: Boolean. If True, the polygon will be resized to fit the output shape if it is bigger.
                                Keeping its aspect ratio. Default: True.
            resize_on_lower: Boolean. If True, the polygon will be resized to fit the one of the output shape bounds, if it is smaller.
                                Keeping its aspect ratio. Default: False.
            resize_pad: Float. The padding to always keep between the polygon and the output shape. Default: 0.05.
    Returns:
        Tuple of 2D coordinates. The corners of the polygon, shifted to the center of the output_shape,
                                in the form ((x1, y1), (x2, y2), ...).
    """
    assert type(polygon) in {np.ndarray, tuple, list}, f"The corners must be a numpy array, tuple or list. Got {type(polygon)}"
    assert all(len(coords) == len(output_shape) for coords in polygon), "The corners must be 2D coordinates"
    assert len(polygon) >= 2, "The polygon must have at least 2 corners"
    assert type(output_shape) in {np.ndarray, tuple, list}, f"The output_shape must be a numpy array or tuple. Got {type(output_shape)}"

    x_min, x_max, y_min, y_max = get_x_y_min_max(polygon=polygon)
    # If polygon is bigger than output_shape, resize it keeping the aspect ratio to match its size with the output_shape bounds
    if resize_on_bigger and (output_shape[0] < x_max-x_min or output_shape[1] < y_max-y_min)\
            or resize_on_lower and (output_shape[0] > x_max-x_min or output_shape[1] > y_max-y_min):
        polygon = resize_polygon(polygon=polygon, output_shape=output_shape, resize_pad=resize_pad)
        x_min, x_max, y_min, y_max = get_x_y_min_max(polygon=polygon)

    # Calculate the center of both the polygon and the output shape
    x_center, y_center = (x_min+x_max)/2, (y_min+y_max)/2
    x_center_output, y_center_output = output_shape[0]/2, output_shape[1]/2
    # Calculate the shift needed to match both centers
    x_shift, y_shift = x_center_output-x_center, y_center_output-y_center
    return tuple((x+x_shift, y+y_shift) for x, y in polygon)

def resize_polygon(polygon: np.ndarray | tuple[tuple[int | float, int | float], ...] |
                   list[list[int | float, int | float], ...],
                   output_shape: np.ndarray | tuple[int | float, int | float] |
                                 list[int | float, int |float],
                   resize_pad: float = 0.) -> tuple[tuple[int | float, int | float], ...]:
    """
    Resize the polygon to fit its maximum size with the bounds of the given output_shape. Keeping its aspect ratio.
    Args:
            polygon: Iterable of 2D coordinates. The corners of the polygon in the form ((x1, y1), (x2, y2), ...).
            output_shape: Tuple of 2 integers or float. The shape of the output element, in the form (width, height).
                            The polygon will be resized to fit this shape.
    Returns:
        Tuple of 2D coordinates. The corners of the polygon, resized to fit the output_shape in a way that the bigger
                                side of the polygon will be the same size as the smaller side of the output_shape.
                                In the form ((x1, y1), (x2, y2), ...).
    """
    assert type(polygon) in {np.ndarray, tuple, list}, f"The corners must be a numpy array, tuple or list. Got {type(polygon)}"
    assert all(len(coords) == len(output_shape) for coords in polygon), "The corners must be 2D coordinates"
    assert len(polygon) >= 2, "The polygon must have at least 2 corners"
    assert 0. <= resize_pad <= (1. - 1e-3), "The resize_pad must be between 0 and 1"
    x_min, x_max, y_min, y_max = get_x_y_min_max(polygon=polygon)
    original_aspect_ratio = (x_max-x_min)/(y_max-y_min)
    x_min, x_max, y_min, y_max = x_min-resize_pad*(x_max-x_min), x_max+resize_pad*(x_max-x_min),\
                                 y_min-resize_pad*(y_max-y_min), y_max+resize_pad*(y_max-y_min)
    # Calculate the ratio of the polygon to the output_shape
    x_ratio, y_ratio = (x_max-x_min)/output_shape[0], (y_max-y_min)/output_shape[1]
    # Take the max_ratio to fit the polygon in the output_shape
    max_ratio = max(x_ratio, y_ratio)
    # Divide the whole polygon by the max_ratio to fit the polygon in the output_shape
    new_polygon = tuple((x/max_ratio, y/max_ratio) for x, y in polygon)
    # Shift to correct the resize pad:
    if resize_pad > 0.:
        x_min, x_max, y_min, y_max = get_x_y_min_max(polygon=new_polygon)
        x_shift, y_shift = resize_pad*(x_max-x_min), resize_pad*(y_max-y_min)
        new_polygon = tuple((x+x_shift, y+y_shift) for x, y in new_polygon)
        final_aspect_ratio = (x_max-x_min)/(y_max-y_min)
        assert np.isclose(original_aspect_ratio, final_aspect_ratio, rtol=1e-3), "The aspect ratio of the polygon should " \
                                                                                 "be the same as the output_shape"
    return new_polygon