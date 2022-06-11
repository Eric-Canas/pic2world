
def distance_in_px_correcting_angle(distance_in_px, angle):
    """
    Correct the distance in pixels to the angle.
    :param distance_in_px:
    :param angle:
    :return:
    """
    return distance_in_px * math.cos(math.radians(angle))