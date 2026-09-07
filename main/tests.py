from django.test import TestCase, Client
from django.contrib.auth.models import User
from main.models import Song, Playlist


class YouTubeExtractionTest(TestCase):

    def test_youtube_id_extraction_various_formats(self):
        song1 = Song(title="Test 1", audio_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        self.assertEqual(song1.get_youtube_video_id(), "dQw4w9WgXcQ")

        song2 = Song(title="Test 2", audio_url="https://youtu.be/dQw4w9WgXcQ")
        self.assertEqual(song2.get_youtube_video_id(), "dQw4w9WgXcQ")

        song3 = Song(title="Test 3", audio_url="https://www.youtube.com/watch?feature=shared&v=dQw4w9WgXcQ&t=10s")
        self.assertEqual(song3.get_youtube_video_id(), "dQw4w9WgXcQ")

        song4 = Song(title="Test 4", audio_url="https://www.youtube.com/shorts/dQw4w9WgXcQ")
        self.assertEqual(song4.get_youtube_video_id(), "dQw4w9WgXcQ")


class ViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="Password123!")
        self.song = Song.objects.create(
            title="Believer",
            artist="Imagine Dragons",
            gerne="Rock",
            audio_url="https://www.youtube.com/watch?v=7wtfhZwyrcc",
            duration="3:24"
        )

    def test_homepage_unauthenticated(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_homepage_authenticated(self):
        self.client.login(username="testuser", password="Password123!")
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Believer")

    def test_ajax_toggle_like(self):
        self.client.login(username="testuser", password="Password123!")
        response = self.client.get(
            f'/like/{self.song.id}/',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "success")
        self.assertTrue(data["liked"])

        # Toggle again -> should be unliked
        response = self.client.get(
            f'/like/{self.song.id}/',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data["liked"])
