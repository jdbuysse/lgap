from django.contrib import admin
from nlp.models import Text

# Register your models here.
# this becomes redundant with the decorator thing below, it seems
# admin.site.register(Text)


@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    # these are properties from the Text model
    list_display = ('id', 'title', 'owner')
    # I guess a subset of the above?
    list_filter = ('title', 'id')

    # I'm not sure what this does yet (from the tutorial and not really explained)
    fieldsets = (
        (None, {
           'fields': ('title', 'id')
        }),
        # ('Availability', {
        #     'fields': ('status', 'due_back', 'borrower')
        # }),
    )

