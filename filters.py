from PIL import Image


def pixelate_image(image_path, pixel_size):
    """
    Pixelate an image.

    Parameters:
    image_path (str): Path to the input image file.
    pixel_size (int): Size of each pixel. Larger values result in stronger pixelation.

    Returns:
    pixelated_image (PIL.Image.Image): Pixelated image.
    """
    # Open the image
    image = Image.open(image_path)

    # Calculate the new size based on pixel_size
    new_width = image.width // pixel_size
    new_height = image.height // pixel_size

    # Resize the image using NEAREST resampling algorithm
    pixelated_image = image.resize((new_width, new_height), Image.NEAREST)

    # Resize the pixelated image back to the original size
    pixelated_image = pixelated_image.resize(image.size, Image.NEAREST)

    return pixelated_image
