from .models import Playlist


def music_context(request):
    """
    Globally provides the logged-in user's playlists and liked song count
    to all templates for the left sidebar navigation.
    """
    if request.user.is_authenticated:
        return {
            'nav_playlists': Playlist.objects.filter(user=request.user).order_by('-id')[:15],
            'nav_liked_count': request.user.liked_songs.count(),
        }
    return {
        'nav_playlists': [],
        'nav_liked_count': 0,
    }
