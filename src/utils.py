import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

def clip_image(img_array):
    """
    Clip all pixel values to the valid image range [0, 255].

    Parameters
    ----------
    img_array : numpy.ndarray
        Image array of any numeric type.

    Returns
    -------
    numpy.ndarray
        uint8 image with values between 0 and 255.
    """

    return np.clip(img_array, 0, 255).astype(np.uint8)


def pad_image(img_array, pad_size):
    """
    Add edge padding to an image.

    Parameters
    ----------
    img_array : numpy.ndarray
        Input image.

    pad_size : int
        Number of pixels to pad on each side.

    Returns
    -------
    numpy.ndarray
        Padded image.
    """

    return np.pad(
        img_array,
        ((pad_size, pad_size),
         (pad_size, pad_size),
         (0, 0)),
        mode="edge"
    )


def normalize_kernel(kernel):
    """
    Normalize a kernel so that its sum becomes 1.

    Parameters
    ----------
    kernel : numpy.ndarray
        Input convolution kernel.

    Returns
    -------
    numpy.ndarray
        Normalized kernel.
    """

    kernel = kernel.astype(np.float32)

    kernel_sum = np.sum(kernel)

    if kernel_sum != 0:
        kernel = kernel / kernel_sum

    return kernel



def apply_kernel(img_array, kernel):
    """
    Apply a convolution kernel to an RGB image.

    Parameters
    ----------
    img_array : numpy.ndarray
        RGB image.

    kernel : numpy.ndarray
        2D convolution kernel.

    Returns
    -------
    numpy.ndarray
        Filtered image.
    """
    
    # Normalize kernel if required
    kernel = normalize_kernel(kernel)

    # Padding size
    pad = kernel.shape[0] // 2

    # Pad image
    padded = pad_image(img_array, pad)

    # Create sliding windows
    windows = sliding_window_view(
        padded,
        kernel.shape,
        axis=(0, 1)
    )
    print("Window Shape :", windows.shape)
    print("Kernel Shape :", kernel.shape)

    test = windows * kernel
    print("After Multiply :", test.shape)

    # (3,3) -> (3,3,1)
    # kernel = kernel[np.newaxis, :, :]
    
    # Convolution
    output = np.sum(
        windows * kernel,
        axis=(2,3)
    )


    return clip_image(output)