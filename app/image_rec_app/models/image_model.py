""" Image model. """

from datetime import datetime
from typing import List, Optional
from image_rec_app.models.image_status_model import ImageStatus


class Image:
    """ Image DB object model. """

    def __init__(self, ImageName: str,
                 Status: ImageStatus,
                 ObjectPath: str = None,
                 ObjectSize: str = None,
                 LabelValue: List[str] = None,
                 TimeAdded: Optional[datetime] = None,
                 TimeUpdated: Optional[datetime] = None):
        self.ImageName = ImageName
        self.ObjectPath = ObjectPath
        self.ObjectSize = ObjectSize
        self.LabelValue = LabelValue
        self.Status = Status
        self.TimeAdded = TimeAdded or datetime.now()
        self.TimeUpdated = TimeUpdated or datetime.now()

    def update_status(self, new_status: ImageStatus):
        """
        Method for updating the status of the image
        and refresh the update time.
        """
        self.Status = new_status
        self.TimeUpdated = datetime.now()
