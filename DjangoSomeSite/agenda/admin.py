from django.contrib import admin
from .models import Event

# Register your models here.


class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date', 'creation_date', 'local')
    list_filter = ('user', 'date')


admin.site.register(Event, EventAdmin)
