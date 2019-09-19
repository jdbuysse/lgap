import uuid  # using this for unique identifiers of texts
from django.db import models
from datetime import date
from django.contrib.auth.models import User


# Create your models here.
# for now this is a dry run where it's just ID and title, eventually will rep a .txt file
class Text(models.Model):
    # idk if I'm gonna use this, but it's a unique ID for a given text
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="unique ID across all user texts")
    title = models.CharField(max_length=200)
    # ForeignKey is a one-to-many association between this model and a User. might not be strictly the right choice
    # for this case but it should work
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        # string for representing the model object
        # honestly not sure what the first part is for/how it looks (copying from tutorial for now)
        return '{0} ({1})'.format(self.id, self.text.title)
