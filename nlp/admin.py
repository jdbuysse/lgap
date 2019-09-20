from django.contrib import admin
from nlp.models import TextInstance, Text

# Register your models here.
admin.site.register(Text)

# this is for displaying properties in 'admin' when you want to add a text
@admin.register(TextInstance)
class TextInstanceAdmin(admin.ModelAdmin):
    # these are properties from the Text model
    list_display = ('id', 'text', 'owner')
    # I guess a subset of the above?
    list_filter = ('text', 'id', 'owner')

    # I'm not sure what this does yet (from the tutorial and not really explained)
    fieldsets = (
        (None, {
           'fields': ('text', 'id', 'owner')
        }),
        # this is the part I don't really grasp ATM, will have to look to docs
        # ('Availability', {
        #     'fields': ('owner', 'id')
        # }),
    )

