from django.contrib import admin
from nlp.models import UploadText

# Register your models here.

# used to be a lot more here, now just the one text upload model
admin.site.register(UploadText)
