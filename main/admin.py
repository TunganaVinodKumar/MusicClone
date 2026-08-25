from django.contrib import admin
from .models import Song, Playlist


# Register your models here.

admin.site.register(Song)


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'user',
        'is_featured',
    )

    list_filter = (
        'is_featured',
    )

    list_editable = (
        'is_featured',
    )

    search_fields = (
        'name',
        'user__username',
    )