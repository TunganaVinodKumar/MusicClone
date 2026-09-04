from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Song(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    gerne = models.CharField(max_length=200)
    audio_url = models.CharField(max_length=300)
    duration = models.CharField(max_length=20)
    cover_image = models.ImageField(upload_to='cover_image/', blank=True, null=True)

    liked_by = models.ManyToManyField(
        User,
        related_name="liked_songs",
        blank=True
    )

    is_popular = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title
    
    def get_youtube_video_id(self):
        """
        Extract the 11-character YouTube video ID from common YouTube URLs.
        """
        import re

        url = (self.audio_url or "").strip()

        if not url:
            return ""

        patterns = [
            r"(?:youtube\.com/watch\?v=)([A-Za-z0-9_-]{11})",
            r"(?:youtu\.be/)([A-Za-z0-9_-]{11})",
            r"(?:youtube\.com/embed/)([A-Za-z0-9_-]{11})",
            r"(?:youtube\.com/shorts/)([A-Za-z0-9_-]{11})",
        ]

        for pattern in patterns:
            match = re.search(pattern, url)

            if match:
                return match.group(1)

        return ""

    def youtube_url_modify(self):
        video_id = self.get_youtube_video_id()

        if not video_id:
            return ""

        return (
            f"https://www.youtube.com/embed/{video_id}"
            f"?autoplay=1&controls=0&enablejsapi=1&playsinline=1"
        )

    @property
    def youtube_video_id(self):
        return self.get_youtube_video_id()
       
class Playlist(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="playlists")
    song = models.ManyToManyField(Song, related_name="playlists")
    is_featured = models.BooleanField(default=False)

    cover_image = models.ImageField(
    upload_to='playlist_covers/',
    blank=True,
    null=True
)

    def __str__(self):
        return f"{self.name} - {self.user}"

# ============================================================
# USER PROFILE
# ============================================================

class UserProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.user.username} Profile"
    
    