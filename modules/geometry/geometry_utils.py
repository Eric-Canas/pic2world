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
    center = np.mean(corners, axis=0, dtype=corners.dtype)
    # Find the angle of each corner
    angles = np.arctan2(corners[:, 1]-center[1], corners[:, 0]-center[0])
    # Order the corners clockwise
    return corners[np.argsort(angles)]

def get_min_max_coords(polygon : np.ndarray | tuple[tuple[int | float, ...], ...] |
                                 list[list[int | float, ...], ...]) -> \
        tuple[tuple[int | float, ...] | np.ndarray, tuple[int | float,...] | np.ndarray]:
    """
    Compute the minimum and maximums for each coordinate of the given N-D polygon.
    Args:
         polygon: Iterable of ND coordinates. The corners of the polygon in the form ((x1, y1,...), (x2, y2, ...), ...).
    Returns:
        Tuple of 2 ND coordinates or numpy array. The minimum and maximums for each coordinate in the form
        ((x_min, y_min, ...), (x_max, y_max, ...)). Given as tuple if polygon is a tuple or list, or numpy array if
        polygon is a numpy array.
    """
    def as_np(polygon: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        return np.min(polygon, axis=0), np.max(polygon, axis=0)

    assert len(polygon) >= 2, "The polygon must have at least 2 corners"
    if type(polygon) is np.ndarray:
        return as_np(polygon=polygon)
    assert type(polygon) in {tuple, list}, f"The corners must be a numpy array, tuple or list. Got {type(polygon)}"
    assert all(len(coords) == len(polygon[0]) for coords in polygon), "The corners must have the same number of dimensions"
    return tuple(min(coord) for coord in zip(*polygon)), tuple(max(coord) for coord in zip(*polygon))

def circumscribed_rectangle(polygon : np.ndarray | tuple[tuple[int | float, ...], ...] |
                                      list[list[int | float, ...], ...],
                            shift_to_coord: int | tuple[int | float, ...] | None = None ) -> \
        tuple[tuple[int | float, ...], ...] | np.ndarray:
    """
    Compute the rectangle that circumscribes the given polygon.
    Args:
         polygon: Iterable of ND coordinates. The corners of the polygon in the form ((x1, y1), (x2, y2), ...).
            shift_to_coord: Integer or tuple of integers. The coordinate to shift the rectangle to. If None, the rectangle
            will be not shifted. If an integer, the rectangle will be shifted to the (Coord, Coord, ...), if a tuple of
            integers, the rectangle must have the same number of dimensions as the shift_to_coord.
    Returns:
        Tuple of 4 ND coordinates or numpy array. The corners of the circumscribed rectangle in the form ((x1, y1,...), (x2, y2,...),
        (x3, y3,...), (x4, y4,...)). Given as tuple if polygon is a tuple or list, or numpy array if polygon is a numpy array.
    """
    def as_np(mins: np.ndarray, maxs: np.ndarray,
                shift_to_coord: np.ndarray | tuple[int | float, ...] | None) ->\
            np.ndarray:
        if shift_to_coord is not None:
            maxs[:], mins[:] = maxs-mins + shift_to_coord, shift_to_coord
        return bbox_to_polygon(bbox=np.append(mins, maxs, axis=0))

    assert len(polygon) >= 2, "The polygon must have at least 2 corners"
    if shift_to_coord is not None:
        if type(shift_to_coord) in {int, np.int16, np.int32, np.int64, float, np.float16, np.float32, np.float64}:
            shift_to_coord = (shift_to_coord,) * len(polygon[0])
        assert len(shift_to_coord) == len(polygon[0]), f"shift_to_coord must have the same number of dimensions as " \
                                                       f"the polygon. Expected {len(polygon[0])}, got {len(shift_to_coord)}"
    mins, maxs = get_min_max_coords(polygon=polygon)
    if type(polygon) is np.ndarray:
        return as_np(mins=mins, maxs=maxs, shift_to_coord=shift_to_coord)
    else:
        assert all(len(coords) == len(polygon[0]) for coords in polygon), "The corners must have the same number of dimensions"
        if shift_to_coord is not None:
            maxs = tuple(maxi - mini + shift for maxi, mini, shift in zip(maxs, mins, shift_to_coord))
            mins = tuple(shift_to_coord)
        return bbox_to_polygon(bbox=mins + maxs)


def bbox_to_polygon(bbox : tuple[int | float, ...] | list[int | float, ...] | np.ndarray)\
        -> tuple[tuple[int | float, ...], ...] | np.ndarray:
    """
    Convert a bounding box in the form (x1, y1, [...], x2, y2, [...]) to a polygon in the form ((x1, y1, [...]),
    (x2, y2, [...]), (x3, y3, [...]), (x4, y4, [...])).
    Args:
        bbox: Iterable of 2N integers or floats. The bounding box in the form (x1, y1, [...], x2, y2, [...]).
              It accepts N-D bounding boxes, for example, for a 2D bounding box, the bounding box is given as
                (x1, y1, x2, y2). For a 3D bounding box, the bounding box is given as (x1, y1, z1, x2, y2, z2).
    Returns:
        Tuple of 4 ND coordinates or numpy array. The corners of the bounding box in the form ((x1, y1,...), (x2, y2,...),
        (x3, y3,...), (x4, y4,...)). Given as tuple if bbox is a tuple or list, or numpy array if bbox is a numpy array.
    """
    def as_np(bbox: np.ndarray) -> np.ndarray:
        return np.array((bbox[0:2], bbox[[2, 1]], bbox[2:], bbox[[0, 3]]), dtype=bbox.dtype)
    assert len(bbox)%2 == 0, f"The bounding box must have an even number of elements. Got {len(bbox)}"

    if type(bbox) is np.ndarray:
        return as_np(bbox=bbox)
    else:
        return ((bbox[0], bbox[1]), (bbox[2], bbox[1]), (bbox[2], bbox[3]), (bbox[0], bbox[3]))

def get_polygon_shape(polygon : np.ndarray | tuple[tuple[int | float, ...], ...] |
                                 list[list[int | float, ...], ...],
                      as_int: bool = False) -> tuple[int | float, ...] | np.ndarray:
    """
    Compute the shape of the given polygon.
    Args:
         polygon: Iterable of ND coordinates. The corners of the polygon in the form ((x1, y1, [...]), (x2, y2, [...]), ...).
         as_int: Boolean. If True, the shape will be returned as integers.
    Returns:
        Tuple of N integers or float. The (width, height, [...]) of the polygon.
    """
    def as_np(mins: np.ndarray, maxs: np.ndarray, as_int32: bool = False) -> np.ndarray:
        shape = maxs-mins
        if as_int32:
            shape = shape.astype(np.int32)
        return shape

    mins, maxs = get_min_max_coords(polygon=polygon)
    if type(polygon) is np.ndarray:
        return as_np(mins=mins, maxs=maxs, as_int32=as_int)
    elif as_int:
        return tuple(int(maxi - mini) for maxi, mini in zip(maxs, mins))
    else:
        return tuple(maxi - mini for maxi, mini in zip(maxs, mins))

def center_polygon(polygon: np.ndarray | tuple[tuple[int | float, ...], ...] | list[list[int | float, ...], ...],
                   output_shape: np.ndarray | tuple[int | float, ...] | list[int | float, ...],
                   resize_on_bigger: bool = True,
                   resize_on_lower: bool = False,
                   resize_pad: float = 0.) -> tuple[tuple[int | float, ...], ...] | np.ndarray:
    """
    Center the coordinates of the polygon in the given shape.
    Args:
            polygon: Iterable of ND coordinates. The corners of the polygon in the form ((x1, y1, [...]),
                    (x2, y2, [...]), ...).
            output_shape: Tuple of N integers or float. The shape of the output element, in the form (width, height, [...]).
                            The polygon will be shifted to be placed in the center of this shape.
            resize_on_bigger: Boolean. If True, the polygon will be resized to fit the output shape if it is bigger.
                                Keeping its aspect ratio. Default: True.
            resize_on_lower: Boolean. If True, the polygon will be resized to fit the one of the output shape bounds, if it is smaller.
                                Keeping its aspect ratio. Default: False.
            resize_pad: Float. The padding to always keep between the polygon and the output shape. Default: 0.05.
    Returns:
        Tuple of ND coordinates. The corners of the polygon, shifted to the center of the output_shape,
                                in the form ((x1, y1, [...]), (x2, y2, [...]), ...).
    """
    def as_np(polygon: np.ndarray, mins: np.ndarray, maxs: np.ndarray, output_shape: np.ndarray | tuple[int | float, ...] |
                                                                list[int | float, ...]) -> np.ndarray:
        centers = (maxs+mins)*0.5
        if type(output_shape) is not np.ndarray:
            output_shape = np.array(output_shape, dtype=centers.dtype)
        elif output_shape.dtype != centers.dtype:
            output_shape = output_shape.astype(dtype=centers.dtype)
        output_centers = output_shape*0.5
        # Calculate the shift needed to match both centers
        shifts = output_centers - centers
        return polygon + shifts

    assert type(polygon) in {np.ndarray, tuple,
                             list}, f"The corners must be a numpy array, tuple or list. Got {type(polygon)}"
    assert len(polygon) >= 2, "The polygon must have at least 2 corners"
    if type(polygon) is np.ndarray:
        assert polygon.ndim == 2, f"The corners must be a 2D array. Got {polygon.ndim}"
        assert polygon.shape[1] == len(output_shape), f"The number of coordinates must match the output shape. " \
                                                      f"Expected {len(output_shape)}, got {polygon.shape[1]}"
    else:
        assert all(len(coords) == len(output_shape) for coords in
                   polygon), "The corners must have the same dimensions as output_shape"
    assert type(output_shape) in {np.ndarray, tuple,
                                  list}, f"The output_shape must be a numpy array or tuple. Got {type(output_shape)}"
    # Call to geometry_utils functions are common for both numpy arrays and tuples
    mins, maxs = get_min_max_coords(polygon=polygon)
    if resize_on_bigger and any(shape < maxi - mini for (shape, maxi, mini) in zip(output_shape, maxs, mins))\
        or resize_on_lower and any(shape > maxi - mini for (shape, maxi, mini) in zip(output_shape, maxs, mins)):
        polygon = fit_polygon_in_shape(polygon=polygon, output_shape=output_shape, resize_pad=resize_pad)
        mins, maxs = get_min_max_coords(polygon=polygon)

    if type(polygon) is np.ndarray:
        return as_np(polygon=polygon, mins=mins, maxs=maxs, output_shape=output_shape)
    else:
        # Calculate the center of both the polygon and the output shape
        centers = tuple(0.5*(maxi + mini) for maxi, mini in zip(maxs, mins))
        output_centers = tuple(0.5*out for out in output_shape)
        # Calculate the shift needed to match both centers
        shifts = tuple(out - center for out, center in zip(output_centers, centers))
        return tuple(tuple(coord+shift for coord, shift in zip(coords, shifts)) for coords in polygon)

def fit_polygon_in_shape(polygon: np.ndarray | tuple[tuple[int | float, ...], ...] | list[list[int | float, ...], ...],
                         output_shape: np.ndarray | tuple[int | float, ...] | list[int | float, ...],
                         resize_pad: float = 0.) -> tuple[tuple[int | float, ...], ...] | np.ndarray:
    """
    Resize the polygon to fit its maximum size with the bounds of the given output_shape. Keeping its aspect ratio.
    Args:
            polygon: Iterable of ND coordinates. The corners of the polygon in the form ((x1, y1, [...]), (x2, y2, [...]), ...).
            output_shape: Tuple of N integers or float. The shape of the output element, in the form (width, height, [...]).
                            The polygon will be resized to fit this shape.
    Returns:
        Tuple of ND coordinates. The corners of the polygon, resized to fit the output_shape in a way that the bigger
                                side of the polygon will be the same size as the smaller side of the output_shape.
                                In the form ((x1, y1, [...]), (x2, y2, [...]), ...).
    """

    def as_np(mins: np.ndarray, maxs: np.ndarray, output_shape: np.ndarray | tuple[int | float, ...] |
                                                                list[int | float, ...],
              polygon: np.ndarray,
              resize_pad: float | np.float32 | np.float64 = 0.) -> np.ndarray:
        if resize_pad > 0.:
            mins, maxs = mins - resize_pad * (maxs - mins), maxs + resize_pad * (maxs - mins)
        max_ratio = np.max((maxs - mins) / output_shape)
        new_polygon = polygon / max_ratio
        if resize_pad > 0.:
            mins, maxs = get_min_max_coords(polygon=new_polygon)
            shifts = resize_pad * (maxs - mins)
            new_polygon = new_polygon + shifts
        return new_polygon

    assert len(polygon) >= 2, "The polygon must have at least 2 corners"
    assert 0. <= resize_pad <= (1. - 1e-3), "The resize_pad must be between 0 and 1"

    mins, maxs = get_min_max_coords(polygon=polygon)
    if type(polygon) is np.ndarray:
        assert polygon.ndim == 2, f"The corners must be a 2D array. Got {polygon.ndim}"
        assert polygon.shape[1] == len(output_shape), f"The number of coordinates must match the output shape. " \
                                                        f"Expected {len(output_shape)}, got {polygon.shape[1]}"
        return as_np(mins=mins, maxs=maxs, output_shape=output_shape, polygon=polygon, resize_pad=resize_pad)
    else:
        assert type(polygon) in {tuple, list}, f"The corners must be a numpy array, tuple or list. Got {type(polygon)}"
        assert all(len(coords) == len(output_shape) for coords in polygon), "The corners must be 2D coordinates"
        if resize_pad > 0.:
            mins = tuple(mini - resize_pad * (maxi - mini) for maxi, mini in zip(maxs, mins))
            maxs = tuple(maxi + resize_pad * (maxi - mini) for maxi, mini in zip(maxs, mins))
        # Calculate the max ratio of the polygon to the output_shape
        max_ratio = max((maxi - mini)/out for maxi, mini, out in zip(maxs, mins, output_shape))
        # Divide the whole polygon by the max_ratio to fit the polygon in the output_shape
        new_polygon = tuple(tuple(coord/max_ratio) for coord in polygon)
        # Shift to correct the resize pad:
        if resize_pad > 0.:
            mins, maxs = get_min_max_coords(polygon=new_polygon)
            shifts = tuple(resize_pad*(maxi - mini) for maxi, mini in zip(maxs, mins))
            new_polygon = tuple(tuple(coord+shift for coord, shift in zip(coords, shifts))
                                for coords in new_polygon)
        return new_polygon

def resize_polygon(polygon: np.ndarray | tuple[tuple[int | float, ...], ...] | list[list[int | float, ...], ...],
                    new_size: np.ndarray | tuple[int | float | None, ...] | list[int | float | None, ...]) -> \
        tuple[tuple[int | float, ...], ...] | np.ndarray:
    """
    Resize each one of the polygon dimensions to the new size.
    Args:
            polygon: Iterable of ND coordinates. The corners of the polygon in the form ((x1, y1, [...]), (x2, y2, [...]), ...).
            new_size: Tuple of N integers or float. The shape of the output element, in the form (width|None, height|None, [...]).
                            The polygon will be resized to fit this shape. If any of new_size axis is None, that
                            dimension will not be resized.
    Returns:
        Tuple of ND coordinates or numpy array. The corners of the polygon, resized to fit the new_size. In the form
         ((x1, y1, [...]), (x2, y2, [...]), ...). If new_size is a numpy array, the output will be a numpy array.
    """
    def as_np(polygon: np.ndarray, mins: np.ndarray, maxs: np.ndarray, new_size: np.ndarray) -> np.ndarray:
        current_size = maxs - mins
        polygon = polygon.copy()
        for i, size in enumerate(new_size):
            if size is not None:
                polygon[:, i] *= (size / current_size[i])
        return polygon

    mins, maxs = get_min_max_coords(polygon=polygon)
    if type(polygon) is np.ndarray:
        assert polygon.ndim == 2, f"The corners must be a 2D array. Got {polygon.ndim}"
        assert polygon.shape[1] == len(new_size), f"The number of coordinates must match the new size. " \
                                                        f"Expected {len(new_size)}, got {polygon.shape[1]}"
        return as_np(polygon=polygon, mins=mins, maxs=maxs, new_size=new_size)
    else:
        assert type(polygon) in {tuple, list}, f"The corners must be a numpy array, tuple or list. Got {type(polygon)}"
        assert all(len(coords) == len(new_size) for coords in polygon), "The corners must be 2D coordinates"
        return tuple(as_np(polygon=coords, mins=mins, maxs=maxs, new_size=new_size) for coords in polygon)