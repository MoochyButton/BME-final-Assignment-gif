########################################
#              Made by                 #
# Sophie Brodkorb & Hauk Erik Jacobsen #
#    s3090191            s3037096      #
########################################
from typing import Callable, Union, Tuple, Sequence, Any
import numpy as np
import cv2
import os


class Tools:

    """
    Tools class is just a selection of tools that is used by other classes
    """
    class ImageTools:
        @staticmethod
        def save_image(image: np.ndarray, path: str) -> None:
            """
            First it normalizes the image then it saves it to the designated path
            :param image:
            :param path:
            """

            image = Tools.ImageTools.normalize_image(image)
            cv2.imwrite(path, image)

        @staticmethod
        def save_numerically_to_folder(image_list: Sequence[np.ndarray], target_path: str,
                                       classifier: str = "") -> None:
            """
            Saves a list of images numerically to a designated folder with an identifier
            :param image_list:  list of images to save
            :param target_path: path to save the images to
            :param classifier:  denotes the class of the image
            """

            for i in range(len(image_list)):
                image_name = f'{i + 1:03d}.png'  # generate 3 digit numerical file name for picture
                Tools.ImageTools.save_image(image_list[i], fr'{target_path}\{classifier}{image_name}')
                print(f"saved image {image_name}")

        @staticmethod
        def load_numerical_list_images(path: str) -> Sequence[np.ndarray]:
            """
            Returns a list of all the images within the path that are named numerically from 000 to 999
            needs to be rewritten to be generalised a bit more
            :param path: str, the path to the images you want to load
            :return list of images: a sequence of numpy arrays (images)
            """
            images = []
            dir_length = os.listdir(path)
            for i in range(len(dir_length)):
                print(i)
                cv2.waitKey(0)
                image = fr'{i + 1:03d}.png'
                cur_image = cv2.imread(fr'{path}\{image}')
                images.append(cur_image)
            return images

        @staticmethod
        def normalize_image(image: np.ndarray) -> np.ndarray:
            """
            This function is used to normalize an image and to make it into uint8
            It's primarily for just in case and is likely not needed for this project
            :param image:
            :return normalized image:
            """
            if image.dtype != np.uint8:
                normalized_image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)
                image_to_save = normalized_image.astype('uint8')
            else:
                image_to_save = image
            return image_to_save

        @staticmethod
        def ensure_3d(image: np.ndarray) -> np.ndarray:
            """
            code from chatgpt, prompt:
            can you make a method that takes an image and turns it into 3d if it isn't?

            ensures that the input image is 3dimensional
            as well as ensures that it has 3 colour channels

            - If the image is 2D (grayscale), it converts it to a 3D image with one channel.
            - If you want to simulate an RGB image from a grayscale, it duplicates the grayscale
              values across three channels.
            - If the image is already 3D, it returns the image unchanged.

            :param image:
            :return 3d image:
            """

            if image.ndim == 2:
                # Image is grayscale (2D), add a third dimension to simulate a single channel
                image_3d = np.stack((image,) * 3, axis=-1)
            elif image.ndim == 3 and image.shape[2] == 1:
                # Image is 3D but has only one channel, you might leave it as is or duplicate to 3 channels
                image_3d = np.concatenate([image] * 3, axis=2)
            else:
                # Image is already 3D with multiple channels
                image_3d = image
            return image_3d

        @staticmethod
        def show_img(image: np.ndarray, header: str = "") -> None:
            """
            method to take care of repeating cv2 code
            just shows an image
            :param image:
            :param header:
            """
            # show image
            cv2.imshow(header, image)
            # wait for any key to pressed
            cv2.waitKey(0)
            # close window
            cv2.destroyAllWindows()

    @staticmethod
    def pause() -> None:
        """
        For debugging if you want to pause the program.
        Made just because Tools.pause() was easier to remember
        Returns nothing, does nothing.
        :return None:
        """
        input("Press Enter to continue...")

    @staticmethod
    def assign_atr(attribute_value: Union[str, Tuple[str, ...]]) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        """
        Decorator to add attributes to methods for easy identification and filtering.
        This can be used to tag methods with specific features or capabilities.
        :rtype: object
        :param attribute_value: any amount of strings inside a tuple representing the attributes to be assigned.
        """
        def decorator(method: Callable) -> Callable:
            """
            assigns the input method with the attribute value
            :param method:  (method) which method to assign attribute
            :return method: (method) assigned method
            """
            # go through all the attributes that you want to assign
            for attr in attribute_value:
                # assign attribute to the method key and value being the same
                setattr(method, attr, attr)
            return method
        return decorator

    @staticmethod
    def get_methods(cls, attribute_value: str) -> list:
        """
        collects all the methods inside the cls class with attributes = attribute_value
        :param cls:             (cls)  which class to look at
        :param attribute_value: (str)  what attribute to look at
        :return:                (list) list of all methods with attribute_value
        """
        # init a list
        methods = []
        # find all the items in class dict
        for name, attr in cls.__dict__.items():
            # if the item has an attribute with the attribute value
            if hasattr(attr, attribute_value):
                # append to methods list
                methods.append(getattr(cls, name))
        return methods

    @staticmethod
    def get_attribute(cls, attr_name) -> Any:
        """
        Returns the attribute that you define using its name
        :param cls:       (cls) the class you want to get attribute from
        :param attr_name: (str) the attribute you want to get returned
        :return the value of the attribute specified by attr_name, if it exists:
        """
        attr = getattr(cls, attr_name, None)
        if attr is None:
            print(f"couldn't find attribute for {cls} under name {attr_name}")
        return attr

    class Counter:
        """
        This class can be added to count labels
        When called it will return the input label
        Add to the counter by using the add_count method
        """
        def __init__(self) -> None:
            """
            init a set for labels stored as strings
            """
            self.counts = {}

        def __call__(self, label: str) -> int:
            """
            Return the current int count for input label
            :param label:  (str) which label to look up the count for
            :return count: (int) the current count of the label
            """
            return self.counts.get(label, 0)

        def add_count(self, label: str, tell: bool = False) -> None:
            """
            Add count to the input label
            :param label: (str)  which label to add count to
            :param tell:  (bool) if to print the current count
            :return None:
            """
            if label in self.counts:
                self.counts[label] += 1
            else:
                self.counts[label] = 0
            if tell:
                print(f"Counter for {label}: {self.counts[label]}")
