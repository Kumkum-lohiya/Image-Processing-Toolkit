import cv2

def rotate_left(img_array):
    """
    Rotate image 90° Left.
    """

    return cv2.rotate(
        img_array,
        cv2.ROTATE_90_COUNTERCLOCKWISE
    )

def rotate_right(img_array):
    """
    Rotate image 90° Right.
    """

    return cv2.rotate(
        img_array,
        cv2.ROTATE_90_CLOCKWISE
    )

def flip_horizontal(img_array):
    """
    Flip image horizontally.
    """

    return cv2.flip(
        img_array,
        1
    )

def flip_vertical(img_array):
    """
    Flip image vertically.
    """

    return cv2.flip(
        img_array,
        0
    )

def crop():
    pass


def resize_image(img_array, width, height):
    """
    Resize image to given width and height.
    """

    return cv2.resize(
        img_array,
        (width, height),
        interpolation=cv2.INTER_LINEAR
    )