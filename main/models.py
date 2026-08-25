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

    def __str__(self):
        return self.title
    
    def youtube_url_modify(self):
        if 'youtu.be' in self.audio_url:
            video_id = self.audio_url.split("/")[-1].split("?si=")[0]
        elif "youtube.com" in self.audio_url:
            video_id = self.audio_url.split("v=")[-1].split("&")[0]

        return f"https://www.youtube.com/embed/{video_id}?autoplay=1&controls=0&enablejsapi=1&playsinline=1"
    @property
    def youtube_video_id(self):
        return self.youtube_url_modify().split("/embed/")[1].split("?")[0]
       
class Playlist(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="playlists")
    song = models.ManyToManyField(Song, related_name="playlists")
    is_featured = models.BooleanField(default=False)

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
    
    