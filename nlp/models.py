import uuid  # using this for unique identifiers of texts
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# this is the real deal accept no imitators
class UploadText(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="unique ID across all user texts")
    # ForeignKey is a one-to-many association between this model and a User. might not be strictly the right choice
    # for this case but it should work
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=40)
    description = models.CharField(max_length=240)
    # no max length for now
    fulltext = models.TextField()

    def __str__(self):
        # formatting that will help with queryset I think. not sure why it's like this
        return '{0} ({1})'.format(self.id, self.title)


