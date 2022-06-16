"""
This module implements a few functions that can be used to interactively request information from the user.
These functions are specially useful for debugging purposes, for example, for selecting image coordinates
before implementing a detector.
Author: Eric Canas
Mail: eric@ericcanas.com
GitHub: https://github.com/Eric-Canas
License: MIT
"""

import numpy as np
from modules.geometry.geometry_utils import order_2d_corners_clockwise
from matplotlib import pyplot as plt
from matplotlib.backend_bases import MouseButton

def draw_polygon_by_clicking(img: np.ndarray, sides: int=4, verbose:bool=False):
    """
    Draw a polygon on an image by clicking on the corners.

    Args:
        img: The image to draw the polygon on
        sides: The number of sides of the polygon
        verbose: Whether to print the coordinates of the corners
    """
    assert img.ndim == 3 or img.ndim == 2, "Image must be a 2D or 3D array"
    assert type(sides) in {int, np.int32, np.int64}, "The number of sides must be at least 2"
    if verbose:
        print("Click on the corners of the polygon")
    # Display the img
    plt.clf()
    plt.imshow(img)
    title = "Click on the {sides} corners. (Right-Click to remove)".format(sides=sides)
    plt.title(title)
    # Get the corners of the polygon by clicking
    polygon = plt.ginput(n=sides, timeout=0, show_clicks=True, mouse_add=MouseButton.LEFT, mouse_pop=MouseButton.RIGHT)
    polygon = np.abs(polygon, dtype=np.float32)
    polygon = order_2d_corners_clockwise(corners=polygon)
    # Draw the polygon
    plt.plot(np.append(polygon[:, 0], polygon[:1, 0], axis=0),
             np.append(polygon[:, 1], polygon[:1, 1], axis=0), 'r-')
    # show an "is that correct?" window with yes and no buttons
    is_correct = yes_no_message_in_plt()
    # If the answer is yes, return the polygon
    if is_correct:
        return polygon
    # If the answer is no, redraw the polygon
    else:
        repeat = yes_no_message_in_plt(msg="Set the points again?", yes="Repeat", no="Cancel", yes_color="yellow")
        if repeat:
            return draw_polygon_by_clicking(img=img, sides=sides, verbose=verbose)
        else:
            return None

def yes_no_message_in_plt(msg: str = "Is that correct?", yes: str = "Yes", no: str = "No",
                          yes_color: str = "green", no_color = "red") -> bool:
    """Display a message with yes and no buttons in the current figure.

    Args:
        msg: The message to display
        yes: The text of the yes button
        no: The text of the no button
    """
    default_button_alpha, default_text_alpha = 0.05, 0.75
    plt.title(msg)
    # Draw two vertical rectangles to separate the buttons, each one occupying half the width of the window
    w, h = plt.gcf().axes[0].get_xlim()[1], plt.gcf().axes[0].get_ylim()[0]
    divisor_line = plt.plot([w/2, w/2], [0, h], 'k-', alpha=default_text_alpha)
    # Draw two filled rectangles to represent the buttons
    yes_rect = plt.fill_between([0, w/2], [0, 0], [h, h], color=yes_color, alpha=default_button_alpha)
    no_rect = plt.fill_between([w/2, w], [0, 0], [h, h], color=no_color, alpha=default_button_alpha)
    # Draw yes and no in the middle of the rectangles
    yes_text = plt.text(w*(1/4), h/2, yes, horizontalalignment='center', verticalalignment='center',
             fontsize=20, color=yes_color, alpha=default_text_alpha)
    no_text = plt.text(w*(3/4), h/2, no, horizontalalignment='center', verticalalignment='center',
             fontsize=20, color=no_color, alpha=default_text_alpha)

    # Wait for the user to click on one of the buttons
    answer = plt.ginput(1, timeout=0, show_clicks=False)[0]
    # Clear all the elements drawn within this function
    # Get the axes of the current figure
    axes = plt.gcf().axes[0]
    # Remove the divisor line
    axes.lines.remove(divisor_line[0])
    # Remove the yes and no rectangles
    axes.collections.remove(yes_rect), axes.collections.remove(no_rect)
    # Remove the yes and no text
    axes.texts.remove(yes_text), axes.texts.remove(no_text)
    accepted = answer[0] < w/2
    plt.title(f"Answer: {yes if accepted else no}")
    return accepted