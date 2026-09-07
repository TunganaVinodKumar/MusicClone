from django.contrib import admin
from .models import Song, Playlist, UserProfile


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'artist',
        'gerne',
        'is_popular',
        'created_at',
    )

    list_filter = (
        'is_popular',
    )

    list_editable = (
        'is_popular',
    )

    search_fields = (
        'title',
        'artist',
        'gerne',
    )


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'user',
        'is_featured',
        'cover_image',
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

    filter_horizontal = (
        'song',
    )

    fields = (
        'name',
        'user',
        'song',
        'is_featured',
        'cover_image',
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'profile_picture',
    )

    search_fields = (
        'user__username',
        'user__email',
    )