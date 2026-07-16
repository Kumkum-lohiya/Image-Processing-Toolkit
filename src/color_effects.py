import cv2
import numpy as np


# ==========================
# NEGATIVE
# ==========================

def apply_negative(img_array):
    """
    Convert image to negative.
    """
    return 255 - img_array


# ==========================
# SEPIA
# ==========================

def apply_sepia(img_array):
    """
    Apply Sepia Effect.
    """

    sepia_filter = np.array([
        [0.272, 0.534, 0.131],
        [0.349, 0.686, 0.168],
        [0.393, 0.769, 0.189]
    ], dtype=np.float32)

    output = cv2.transform(
        img_array.astype(np.float32),
        sepia_filter
    )

    return np.clip(output, 0, 255).astype(np.uint8)


# ==========================
# THRESHOLD
# ==========================

def apply_threshold(img_array, threshold_value):
    """
    Apply Binary Threshold.
    """

    gray = cv2.cvtColor(
        img_array,
        cv2.COLOR_RGB2GRAY
    )

    _, output = cv2.threshold(
        gray,
        threshold_value,
        255,
        cv2.THRESH_BINARY
    )

    return cv2.cvtColor(
        output,
        cv2.COLOR_GRAY2RGB
    )


# ==========================
# GAMMA CORRECTION
# ==========================

def apply_gamma(img_array, gamma_value):
    """
    Apply Gamma Correction.
    """

    if gamma_value <= 0:
        return img_array

    inv_gamma = 1.0 / gamma_value

    table = np.array([
        ((i / 255.0) ** inv_gamma) * 255
        for i in np.arange(256)
    ]).astype("uint8")

    return cv2.LUT(
        img_array,
        table
    )