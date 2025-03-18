import uuid

from django.db import models


class BaseModel(models.Model):
    """
    Base model for all the models in the application.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
