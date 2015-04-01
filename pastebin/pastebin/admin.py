from django.contrib import admin
from .models import Paste, Syntax

@admin.register(Paste)
class Paste(admin.ModelAdmin):
    exclude = ('hash',)
    read_only_fields = ('hash',)

    list_display = ('hash', 'syntax', 'created')

    list_filter = ('created', 'syntax__name')


admin.site.register(Syntax)