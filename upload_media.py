import os
from pathlib import Path

import cloudinary
import cloudinary.uploader
from django import setup

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Mymusic.settings")
setup()

from django.conf import settings
from main.models import Song, Playlist, UserProfile


cloudinary.config(
    cloud_name=os.environ["CLOUDINARY_CLOUD_NAME"],
    api_key=os.environ["CLOUDINARY_API_KEY"],
    api_secret=os.environ["CLOUDINARY_API_SECRET"],
)


BASE_DIR = Path(settings.BASE_DIR)
MEDIA_ROOT = BASE_DIR / "media"


def upload_file(relative_path):
    local_file = MEDIA_ROOT / relative_path

    if not local_file.exists():
        print(f"MISSING: {relative_path}")
        return False

    result = cloudinary.uploader.upload(
        str(local_file),
        public_id=Path(relative_path).with_suffix("").as_posix(),
        resource_type="image",
        overwrite=True,
    )

    print(f"UPLOADED: {relative_path}")
    print(f"         {result['secure_url']}")
    return True


paths = set()

for song in Song.objects.all():
    if song.cover_image:
        paths.add(str(song.cover_image))

for playlist in Playlist.objects.all():
    if playlist.cover_image:
        paths.add(str(playlist.cover_image))

for profile in UserProfile.objects.all():
    if profile.profile_picture:
        paths.add(str(profile.profile_picture))


print(f"Files to upload: {len(paths)}")
print()

success = 0

for path in sorted(paths):
    if upload_file(path):
        success += 1

print()
print(f"Uploaded successfully: {success}/{len(paths)}")