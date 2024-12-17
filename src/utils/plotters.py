import numpy as np
import plotly.express as px


class ImageVisualizer:
    def __init__(self, width: int = 800, height: int = 600):
        """
        Initializes the ImageVisualizer with configurable display size.

        Args:
            width (int): Width of the image display.
            height (int): Height of the image display.
        """
        self.width = width
        self.height = height

    def display_images(self, images: list[np.ndarray]):
        """
        Displays a list of images with configured size.

        Args:
            images (list of np.ndarray): List of images to display.
        """
        for idx, img in enumerate(images):
            print(f"Displaying Image {idx+1}: Shape={img.shape}")
            px.imshow(
                img, title=f"Image {idx+1}", width=self.width, height=self.height
            ).show()
