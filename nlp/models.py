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
    fulltext = models.TextField(max_length=100000)

    def __str__(self):
        # formatting that I should change later because it's long and confusing to have the ID there
        return self.title


# practice run for file storage work
class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class ByteText(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="unique ID across all user texts")
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=40)
    bytefile = models.FileField() # is FileField what I want?

    def __str__(self):
        # formatting that I should change later because it's long and confusing to have the ID there
        return self.title

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    pdf = models.FileField(upload_to='books/pdfs/')

    def __str__(self):
        return self.title

