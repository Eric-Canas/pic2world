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
