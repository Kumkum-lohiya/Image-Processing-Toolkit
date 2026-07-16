import cv2
import numpy as np

from src.utils import (
    clip_image,
    apply_kernel
)

def grayscale(img_array):
    """
    Convert RGB image to Grayscale.

    Parameters
    ----------
    img_array : numpy.ndarray

    Returns
    -------
    numpy.ndarray
    """

    gray = (
        0.299 * img_array[:, :, 0]
        + 0.587 * img_array[:, :, 1]
        + 0.114 * img_array[:, :, 2]
    )

    gray = gray.astype(np.uint8)

    gray = np.stack(
        (gray, gray, gray),
        axis=2
    )

    return gray

def adjust_brightness(img_array, value):
    """
    Increase or decrease image brightness.
    """

    img_array = img_array.astype(np.int16)

    img_array = img_array + value

    return clip_image(img_array)

def adjust_contrast(img_array, value):
    """
    Adjust image contrast.
    """

    factor = (
        259 * (value + 255)
    ) / (
        255 * (259 - value)
    )

    result = factor * (
        img_array.astype(np.float32) - 128
    ) + 128

    return clip_image(result)

# def apply_blur(img_array, blur_value):
    # """
    # Apply Box Blur to an image.
    # """

    # if blur_value == 0:
    #     return img_array

    # kernel_size = 2 * blur_value + 1

    # blur_kernel = np.ones(
    #     (kernel_size, kernel_size),
    #     dtype=np.float32
    # )

    # return apply_kernel(
    #     img_array,
    #     blur_kernel
    # )

def apply_blur(img_array, blur_value):

    if blur_value == 0:
        return img_array

    kernel_size = 2 * blur_value + 1

    return cv2.GaussianBlur(
        img_array,
        (kernel_size, kernel_size),
        0
    )
# def apply_sharpen(img_array, sharpen_value):
#     """
#     Apply Sharpen filter.
#     """

#     if sharpen_value == 0:
#         return img_array

#     kernel = np.array([
#         [0, -1, 0],
#         [-1, 5 + sharpen_value, -1],
#         [0, -1, 0]
#     ], dtype=np.float32)

#     return apply_kernel(
#         img_array,
#         kernel
#     )


def apply_sharpen(img_array, sharpen_value):

    if sharpen_value == 0:
        return img_array

    kernel = np.array([
        [0, -1, 0],
        [-1, 5 + sharpen_value, -1],
        [0, -1, 0]
    ], dtype=np.float32)

    return cv2.filter2D(
        img_array,
        -1,
        kernel
    )