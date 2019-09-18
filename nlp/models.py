import uuid # using this for unique identifiers of texts
from django.db import models
from datetime import date
from django.contrib.auth.models import User


# Create your models here.
# for now this is a dry run where it's just ID and title, eventually will rep a .txt file
class Text(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="unique ID across all user texts")
    title = models.CharField(max_length=200)

    def __str__(self):
        # string for representing the model object
        # honestly not sure what the first part is for (copying from tutorial for now)
        return '{0} ({1})'.format(self.id, self.title)
