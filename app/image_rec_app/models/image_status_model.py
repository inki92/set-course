""" Model with status string. """

from enum import Enum


class ImageStatus(Enum):
    """ Class with image status string values. """
    NEW = "NEW"
    RECOGNITION_FAILED = "RECOGNITION_FAILED"
    RECOGNITION_COMPLETED = "RECOGNITION_COMPLETED"
