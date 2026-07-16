# print("App Started")
import customtkinter as ctk
from tkinter import filedialog, Canvas
from PIL import Image,ImageTk
import numpy as np

from src.basic_filters import (
    grayscale,
    adjust_brightness,
    adjust_contrast,
    apply_blur,
    apply_sharpen
   
)

from src.color_effects import (
    apply_negative,
    apply_sepia,
    apply_threshold,
    apply_gamma
)

from src.transformations import (
    rotate_left,
    rotate_right,
    flip_horizontal,
    flip_vertical,
    resize_image,
    # crop_image
)

current_image = None
original_array = None      # Full Resolution
preview_array = None       # Processing Image
current_array = None

is_grayscale = False

brightness_value = 0
contrast_value = 0
blur_value = 0
sharpen_value = 0

negative_enabled = False
sepia_enabled = False

threshold_enabled = False
gamma_enabled = False

threshold_value = 127
gamma_value = 1.0

rotation_angle = 0

flip_horizontal_enabled = False
flip_vertical_enabled = False

crop_mode = False

crop_start_x = 0
crop_start_y = 0

crop_end_x = 0
crop_end_y = 0

crop_rectangle = None

def display_image(img_array):

    global current_image

    image = Image.fromarray(img_array)

    image.thumbnail((600,450))

    current_image = ImageTk.PhotoImage(image)

    canvas.delete("all")

    canvas.create_image(
    0,
    0,
    image=current_image,
    anchor="nw"
    )

# ==================================== 
# SELECT IMAGE
# ====================================


def select_image():

    global current_image
    global current_array
    global original_array
    global preview_array
    global is_grayscale
    global brightness_value
    global contrast_value
    global blur_value
    global sharpen_value
    global negative_enabled
    global sepia_enabled
    global threshold_value
    global gamma_value

    path = filedialog.askopenfilename(
        filetypes=[
            ("Image Files", "*.png *.jpg *.jpeg")
        ]
    )

    if not path:
        return

    image = Image.open(path).convert("RGB")

    preview = image.copy()
    preview.thumbnail((700,700))

    preview_np = np.array(preview)

    original_array = preview_np.copy()
    preview_array = preview_np.copy()
    current_array = preview_np.copy()

# Reset all filter values
    is_grayscale = False
    brightness_value = 0
    contrast_value = 0
    blur_value = 0
    sharpen_value = 0
    negative_enabled = False
    sepia_enabled = False

    threshold_value = 127
    gamma_value = 1.0

    # Reset sliders
    brightness_slider.set(0)
    contrast_slider.set(0)
    blur_slider.set(0)
    sharpen_slider.set(0)
    threshold_slider.set(127)
    gamma_slider.set(1)

    display_image(preview_array)

def update_image():

    global current_array
    

    if preview_array is None:
        return

    image = preview_array.copy()

   

    if is_grayscale:
        image = grayscale(image)

    image = adjust_brightness(image, brightness_value)

    image = adjust_contrast(image, contrast_value)

    if negative_enabled:
        image = apply_negative(image)

    if sepia_enabled:
            image = apply_sepia(image)

    if threshold_enabled:
        image = apply_threshold(
        image,
        threshold_value
    )

    if gamma_enabled:
        image = apply_gamma(
        image,
        gamma_value
    )

    image = apply_blur(
            image,
            blur_value
        )

    image = apply_sharpen(
            image,
            sharpen_value
        )
    
    # -------------------------
    # Transformations
    # -------------------------

    if rotation_angle == 90:
        image = rotate_right(image)

    elif rotation_angle == 180:
        image = rotate_right(
            rotate_right(image)
        )

    elif rotation_angle == 270:
        image = rotate_left(image)

    if flip_horizontal_enabled:
        image = flip_horizontal(image)

    if flip_vertical_enabled:
        image = flip_vertical(image)  

    current_array = image

    display_image(current_array)

# ==========================================
# SAVE IMAGE
# ==========================================

def save_image():

    if current_array is None:
        print("No image to save")
        return

    path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[
            ("PNG Image","*.png"),
            ("JPEG Image","*.jpg")
        ]
    )

    if not path:
        return

    image = Image.fromarray(current_array)

    image.save(path)

    print("Image Saved Successfully")

# ==============================================
# RESET IMAGE
# =============================================
    
def reset_image():

    global current_array
    global preview_array 
    global original_array
    global is_grayscale
    global brightness_value
    global contrast_value
    global blur_value
    global sharpen_value
    global negative_enabled
    global sepia_enabled
    global threshold_value
    global gamma_value
    global rotation_angle
    global flip_horizontal_enabled
    global flip_vertical_enabled

    if original_array is None:
        return

    # Reset all values
    is_grayscale = False
    brightness_value = 0
    contrast_value = 0
    blur_value = 0
    sharpen_value = 0

    # Reset sliders
    brightness_slider.set(0)
    contrast_slider.set(0)
    blur_slider.set(0)
    sharpen_slider.set(0)

    negative_enabled = False
    sepia_enabled = False

    threshold_value = 127
    gamma_value = 1.0

    threshold_slider.set(127)
    gamma_slider.set(1)

    # Restore original preview image
    

    # Display image
    gray_button.configure(text="Grayscale")

    negative_button.configure(text="Negative")

    sepia_button.configure(text="Sepia")

    threshold_button.configure(text="Threshold")

    gamma_button.configure(text="Gamma")

    flip_horizontal_button.configure(
    text="↔ Flip Horizontal"
    )

    flip_vertical_button.configure(
        text="↕ Flip Vertical"
    )
    rotation_angle = 0

    flip_horizontal_enabled = False
    flip_vertical_enabled = False

    current_array = original_array.copy()
    preview_array = original_array.copy()

   

    update_image()

# Theme
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")


# Main Window
app = ctk.CTk()

app.title("Image Processing Toolkit")
app.geometry("1000x700")


# Heading
title = ctk.CTkLabel(
    app,
    text="🖼 Image Processing Toolkit",
    font=("Arial", 30, "bold")
)

title.pack(pady=20)

content_frame = ctk.CTkFrame(
    app,
    fg_color="transparent"
)

content_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=10
)

left_frame = ctk.CTkFrame(
    content_frame,
    fg_color="transparent"
)

left_frame.pack(
    side="left",
    padx=30,
    pady=20,
    expand=True
)

right_frame = ctk.CTkFrame(
    content_frame,
    width=250,
    corner_radius=15
)

right_frame.pack_propagate(False)

right_frame.pack(
    side="right",
    fill="y",
    padx=20,
    pady=20
)

# ==========================================
# Collapsible Section Creator
# ==========================================

def create_section(parent, title):

    # Container
    container = ctk.CTkFrame(parent, fg_color="transparent")
    container.pack(fill="x", padx=5, pady=(5,5))

    # Toggle Button
    button = ctk.CTkButton(
        container,
        text="▶" + title,
        anchor="w",
        fg_color="transparent",
        hover_color=("gray85", "gray25"),
        text_color=("black", "white"),
        height=35
    )

    button.pack(fill="x")

    # Content Frame
    frame = ctk.CTkFrame(container)
   # frame initially hidden

    expanded = False

    def toggle():
        nonlocal expanded

        if expanded:

            frame.pack_forget()
            button.configure(text="▶ " + title)

        else:

            frame.pack(fill="x", pady=(2,5))
            button.configure(text="▼ " + title)

        expanded = not expanded

    button.configure(command=toggle)

    return frame


image_frame = ctk.CTkFrame(
    left_frame,
    width=620,
    height=470,
    corner_radius=15
)

image_frame.pack(pady=20)

def start_crop(event):

    global crop_start_x
    global crop_start_y
    global crop_rectangle

    if not crop_mode:
        return

    crop_start_x = event.x
    crop_start_y = event.y

    # Purana rectangle hata do
    canvas.delete("crop")

    crop_rectangle = canvas.create_rectangle(
        crop_start_x,
        crop_start_y,
        crop_start_x,
        crop_start_y,
        outline="red",
        width=2,
        tags="crop"
    )

def drag_crop(event):

    if not crop_mode:
        return

    canvas.coords(
        crop_rectangle,
        crop_start_x,
        crop_start_y,
        event.x,
        event.y
    )

def end_crop(event):

    global crop_end_x
    global crop_end_y
    global current_array
    global preview_array
    global crop_mode

    if not crop_mode:
        return

    crop_end_x = event.x
    crop_end_y = event.y

    # Coordinates sort karo
    x1 = min(crop_start_x, crop_end_x)
    x2 = max(crop_start_x, crop_end_x)

    y1 = min(crop_start_y, crop_end_y)
    y2 = max(crop_start_y, crop_end_y)

    # Minimum size check
    if (x2 - x1) < 5 or (y2 - y1) < 5:
        canvas.delete("crop")
        return

    # Crop
    cropped = current_array[y1:y2, x1:x2]

    if cropped.size == 0:
        return

    current_array = cropped.copy()
    preview_array = cropped.copy()

    display_image(current_array)

    canvas.delete("crop")

    crop_mode = False

    crop_button.configure(text="✂ Crop")


canvas = Canvas(
    image_frame,
    width=600,
    height=450,
    bg="#2b2b2b",
    highlightthickness=0
)

canvas.place(
    relx=0.5,
    rely=0.5,
    anchor="center"
)

canvas.bind("<Button-1>", start_crop)

canvas.bind("<B1-Motion>", drag_crop)

canvas.bind("<ButtonRelease-1>", end_crop)

# Button
button = ctk.CTkButton(
    left_frame,
    text="Select Image",
    width=220,
    height=40,
    command=select_image
)

button.pack(pady=(0,20))

bottom_button_frame = ctk.CTkFrame(
    left_frame,
    fg_color="transparent"
)

bottom_button_frame.pack(pady=(0,20))

save_button = ctk.CTkButton(
    bottom_button_frame,
    text="💾 Save",
    width=120,
    height=35,
    command=save_image
)

save_button.pack(side="left", padx=10)

reset_button = ctk.CTkButton(
    bottom_button_frame,
    text="🔄 Reset",
    width=120,
    height=35,
    command=reset_image
)

reset_button.pack(side="left", padx=10)

basic_frame = create_section(
    right_frame,
    "Basic Filters"
)

def toggle_grayscale():

    global is_grayscale

    is_grayscale = not is_grayscale

    if is_grayscale:
        gray_button.configure(text="Original")
    else:
        gray_button.configure(text="Grayscale")

    update_image()

gray_button = ctk.CTkButton(
    basic_frame,
    text="Grayscale",
    width=160,
    height=35,
    command=toggle_grayscale
)

gray_button.pack(pady=10)


def change_brightness(value):

    global brightness_value

    brightness_value = int(value)

    update_image()

brightness_label = ctk.CTkLabel(
    basic_frame,
    text="Brightness"
)

brightness_label.pack(pady=(25,5))

brightness_slider = ctk.CTkSlider(
    basic_frame,
    from_=-100,
    to=100,
    width=180,
    command=change_brightness
)

brightness_slider.set(0)

brightness_slider.pack(pady=10)

def change_contrast(value):

    global contrast_value

    contrast_value = int(value)

    update_image()

contrast_label = ctk.CTkLabel(
    basic_frame,
    text="Contrast"
)

contrast_label.pack(pady=(20,5))

contrast_slider = ctk.CTkSlider(
    basic_frame,
    from_=-100,
    to=100,
    width=180,
    command=change_contrast
)

contrast_slider.set(0)
contrast_slider.pack(pady=10)

def change_blur(value):

    global blur_value

    blur_value = int(value)

    update_image()

blur_label = ctk.CTkLabel(
    basic_frame,
    text="Blur"
)

blur_label.pack(pady=(20,5))

blur_slider = ctk.CTkSlider(
    basic_frame,
    from_=0,
    to=5,
    number_of_steps=5,
    width=180,
    command=change_blur
)

blur_slider.set(0)

blur_slider.pack(pady=10)


def change_sharpen(value):

    global sharpen_value

    sharpen_value = int(value)

    update_image()

sharpen_label = ctk.CTkLabel(
    basic_frame,
    text="Sharpen"
)

sharpen_label.pack(pady=(8,2))

sharpen_slider = ctk.CTkSlider(
    basic_frame,
    from_=0,
    to=5,
    number_of_steps=5,
    width=180,
    command=change_sharpen
)

sharpen_slider.set(0)

sharpen_slider.pack(pady=(0,8))


# ==========================
# Colour 
# ==========================

color_frame = create_section(
    right_frame,
    "Color Effects"
)

def toggle_negative():

    global negative_enabled
    global sepia_enabled

    negative_enabled = not negative_enabled

    if negative_enabled:
        sepia_enabled = False
        sepia_button.configure(text="Sepia")
        negative_button.configure(text="Original")
    else:
        negative_button.configure(text="Negative")

    update_image()

negative_button = ctk.CTkButton(
    color_frame,
    text="Negative",
    width=180,
    height=35,
    command=toggle_negative
)

negative_button.pack(pady=8)

def toggle_sepia():

    global sepia_enabled
    global negative_enabled

    sepia_enabled = not sepia_enabled

    if sepia_enabled:
        negative_enabled = False
        negative_button.configure(text="Negative")
        sepia_button.configure(text="Original")
    else:
        sepia_button.configure(text="Sepia")

    update_image()

sepia_button = ctk.CTkButton(
    color_frame,
    text="Sepia",
    width=180,
    height=35,
    command=toggle_sepia
)

sepia_button.pack(pady=8)

def toggle_threshold():

    global threshold_enabled

    threshold_enabled = not threshold_enabled

    if threshold_enabled:
        threshold_button.configure(text="Original")
    else:
        threshold_button.configure(text="Threshold")

    update_image()

threshold_button = ctk.CTkButton(
    color_frame,
    text="Threshold",
    command=toggle_threshold,
    width=180
)

threshold_button.pack(pady=(15,5))

def change_threshold(value):

    global threshold_value

    threshold_value = int(value)

    update_image()

threshold_slider = ctk.CTkSlider(
    color_frame,
    from_=0,
    to=255,
    width=180,
    command=change_threshold
)

threshold_slider.set(127)

threshold_slider.pack(pady=8)

def toggle_gamma():

    global gamma_enabled

    gamma_enabled = not gamma_enabled

    if gamma_enabled:
        gamma_button.configure(text="Original")
    else:
        gamma_button.configure(text="Gamma")

    update_image()

gamma_button = ctk.CTkButton(
    color_frame,
    text="Gamma",
    command=toggle_gamma,
    width=180
)

gamma_button.pack(pady=(15,5))



def change_gamma(value):

    global gamma_value

    gamma_value = float(value)

    update_image()

gamma_slider = ctk.CTkSlider(
    color_frame,
    from_=1,
    to=5,
    number_of_steps=40,
    width=180,
    command=change_gamma

)

gamma_slider.set(1)

gamma_slider.pack(pady=(0,15))


# ==========================
# TRANSFORMATIONS
# ==========================

transform_frame = create_section(
    right_frame,
    "Transformations"
)

def rotate_left_image():

    global rotation_angle

    if preview_array is None:
        return

    rotation_angle = (rotation_angle - 90) % 360

    update_image()

rotate_left_button = ctk.CTkButton(
    transform_frame,
    text="↺ Rotate Left",
    width=180,
    height=35,
    command=rotate_left_image
)

rotate_left_button.pack(pady=5)

def rotate_right_image():

    global rotation_angle

    if preview_array is None:
        return

    rotation_angle = (rotation_angle + 90) % 360

    update_image()

rotate_right_button = ctk.CTkButton(
    transform_frame,
    text="↻ Rotate Right",
    width=180,
    height=35,
    command= rotate_right_image
)

rotate_right_button.pack(pady=5)

def toggle_flip_horizontal():

    global flip_horizontal_enabled

    if preview_array is None:
        return

    flip_horizontal_enabled = not flip_horizontal_enabled

    if flip_horizontal_enabled:
        flip_horizontal_button.configure(
            text="Original"
        )
    else:
        flip_horizontal_button.configure(
            text="↔ Flip Horizontal"
        )

    update_image()

flip_horizontal_button = ctk.CTkButton(
    transform_frame,
    text="↔ Flip Horizontal",
    width=180,
    height=35,
    command=toggle_flip_horizontal
)

flip_horizontal_button.pack(pady=5)

def toggle_flip_vertical():

    global flip_vertical_enabled

    if preview_array is None:
        return

    flip_vertical_enabled = not flip_vertical_enabled

    if flip_vertical_enabled:
        flip_vertical_button.configure(
            text="Original"
        )
    else:
        flip_vertical_button.configure(
            text="↕ Flip Vertical"
        )

    update_image()

flip_vertical_button = ctk.CTkButton(
    transform_frame,
    text="↕ Flip Vertical",
    width=180,
    height=35,
    command=toggle_flip_vertical
)

flip_vertical_button.pack(pady=5)

def open_resize_window():

    if current_array is None:
        return

    resize_window = ctk.CTkToplevel(app)
    resize_window.title("Resize Image")
    resize_window.geometry("300x220")
    resize_window.transient(app)      # Parent app ke upar open hogi
    resize_window.grab_set()          # Jab tak band na ho, sirf isi window par focus rahega
    resize_window.focus_force()       # Direct focus isi window par aayega

    ctk.CTkLabel(
        resize_window,
        text="Width"
    ).pack(pady=(15,5))

    width_entry = ctk.CTkEntry(resize_window)
    width_entry.pack()

    ctk.CTkLabel(
        resize_window,
        text="Height"
    ).pack(pady=(10,5))

    height_entry = ctk.CTkEntry(resize_window)
    height_entry.pack()

    height, width = current_array.shape[:2]

    width_entry.insert(0, str(width))
    height_entry.insert(0, str(height))

    ctk.CTkButton(
        resize_window,
        text="Resize",
        command=lambda: apply_resize(
            width_entry.get(),
            height_entry.get(),
            resize_window
        )
    ).pack(pady=20)

def apply_resize(width, height, window):

    global current_array
    global preview_array
    global original_array

    try:
        width = int(width)
        height = int(height)

        current_array = resize_image(
        current_array,
        width,
        height
    )

        preview_array = current_array.copy()
        original_array = current_array.copy()

        display_image(current_array)
        window.destroy()

    except ValueError:
        print("Invalid Width or Height")

# def resize_current_image():

#     global current_array

#     if current_array is None:
#         return

#     current_array = resize_image(
#         current_array,
#         500,
#         500
#     )

#     display_image(current_array)

resize_button = ctk.CTkButton(
    transform_frame,
    text="📏 Resize",
    width=180,
    height=35,
    command=open_resize_window
)

resize_button.pack(pady=5)



def toggle_crop():

    global crop_mode

    crop_mode = not crop_mode

    if crop_mode:
        crop_button.configure(text="Cancel Crop")
    else:
        crop_button.configure(text="Crop")

crop_button = ctk.CTkButton(
    transform_frame,
    text="✂ Crop",
    width=180,
    height=35,
    command=toggle_crop
)

crop_button.pack(pady=(5,10))

# Start Application
app.mainloop()