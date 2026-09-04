from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Song, Playlist, UserProfile
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from random import choice, shuffle as random_shuffle
import re

# ============================================================
# HOME PAGE
# ============================================================

# Home page
def index(request):

    if not request.user.is_authenticated:
        return render(
            request,
            "main/master_home.html"
        )
    
    songs = Song.objects.all()

    # --------------------------------------------------------
    # Popular Songs - remove duplicate title + artist entries
    # --------------------------------------------------------

    popular_songs = Song.objects.filter(
    is_popular=True
).order_by('-id')[:15]
    recent_songs = Song.objects.order_by(
    '-created_at'
)[:6]

    

    featured_playlists = Playlist.objects.filter(
        is_featured=True
        )

    search_songs = list(
        songs.values(
                'id',
                'title',
                'artist',
                'gerne'
            ) 
)

    search_query = request.GET.get('q', '').strip()

    if search_query:
        search_results = songs.filter(
            Q(title__icontains=search_query) |
            Q(artist__icontains=search_query) |
            Q(gerne__icontains=search_query)
        )
    else:
        search_results = Song.objects.none()

    play_song_id = request.GET.get('play', None)

    shuffle_mode = request.GET.get('shuffle') == 'true'

    play_song = None
    player_origin = request.build_absolute_uri('/').rstrip('/')
    previous_song = None
    next_song = None
    shuffle_song = None
    upcoming_songs = []
    youtube_queue = []

    playlists = Playlist.objects.none()

    # User playlists
    if request.user.is_authenticated:

        playlists = Playlist.objects.filter(
            user=request.user
        )

        # Add song to playlist
        if request.method == "POST":

            song_id = request.POST.get('song_id')
            playlist_id = request.POST.get('playlist_id')

            if song_id and playlist_id:

                playlist = get_object_or_404(
                    Playlist,
                    id=playlist_id,
                    user=request.user
                )

                song = get_object_or_404(
                    Song,
                    id=song_id
                )

                if playlist.song.filter(pk=song.pk).exists():
                    messages.info(
                        request,
                        f'"{song.title}" is already in "{playlist.name}".'
    )
                else:
                    playlist.song.add(song)

                    messages.success(
                        request,
                        f'Added "{song.title}" to "{playlist.name}".'
    )
                
                return redirect('index')


    # Currently playing song
    if play_song_id:

        play_song = get_object_or_404(
            Song,
            id=play_song_id
        )

        player_origin = request.build_absolute_uri('/')
        player_origin = player_origin.rstrip('/')

        # Convert songs into a list
        song_list = list(songs)

        try:
            current_index = song_list.index(play_song)

            upcoming_songs = (
                song_list[current_index + 1:]
                + song_list[:current_index]
            )

            if shuffle_mode:
                random_shuffle(upcoming_songs)
    

            youtube_queue = [play_song] + upcoming_songs

            # Previous song
            if current_index > 0:
                previous_song = song_list[current_index - 1]
            else:
                previous_song = song_list[-1]

            # Next song
            if current_index < len(song_list) - 1:
                next_song = song_list[current_index + 1]
            else:
                next_song = song_list[0]

        except ValueError:
            pass

        # Shuffle
        possible_shuffle_songs = [
            song for song in song_list
            if song != play_song
        ]

        if possible_shuffle_songs:
            shuffle_song = choice(
                possible_shuffle_songs
            )


    return render(
        request,
        'main/index.html',
        {
            'songs': songs,

            'search_songs': search_songs,
            'popular_songs': popular_songs,
            'recent_songs': recent_songs,

            'search_query': search_query,
            'search_results': search_results,
            'featured_playlists': featured_playlists,

            'play_song': play_song,
            'playlists': playlists,
            'player_origin': player_origin,

            # Player
            'previous_song': previous_song,
            'next_song': next_song,
            'shuffle_song': shuffle_song,
            'shuffle_mode': shuffle_mode,
            'upcoming_songs': upcoming_songs,
            'youtube_queue': youtube_queue,
            
        }
    )


# ============================================================
# LIKE / UNLIKE SONG
# ============================================================

def toggle_like(request, song_id):

    if not request.user.is_authenticated:
        return redirect('login_user')

    song = get_object_or_404(Song, id=song_id)

    if song.liked_by.filter(id=request.user.id).exists():
        song.liked_by.remove(request.user)
    else:
        song.liked_by.add(request.user)

    return redirect(request.META.get('HTTP_REFERER', 'index'))


# ============================================================
# LIKED SONGS
# ============================================================

@login_required
def liked_songs(request):

    liked_songs = request.user.liked_songs.all()

    return render(
        request,
        'main/liked_songs.html',
        {
            'liked_songs': liked_songs,
        }
    )



# ============================================================
# REGISTER USER
# ============================================================

# Register user
def register_user(request):

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        password2 = request.POST.get("password2", "")

        # -----------------------------
        # Username validation
        # -----------------------------

        if not username:
            return render(
                request,
                "main/register_user.html",
                {
                    "error": "Username is required.",
                    "username": username
                }
            )

        if len(username) < 4:
            return render(
                request,
                "main/register_user.html",
                {
                    "error": "Username must contain at least 4 characters.",
                    "username": username
                }
            )

        if len(username) > 20:
            return render(
                request,
                "main/register_user.html",
                {
                    "error": "Username cannot contain more than 20 characters.",
                    "username": username
                }
            )

        if not re.fullmatch(r"[A-Za-z0-9_]+", username):
            return render(
                request,
                "main/register_user.html",
                {
                    "error": "Username can contain only letters, numbers and underscore (_).",
                    "username": username
                }
            )

        # -----------------------------
        # Check duplicate username
        # -----------------------------

        if User.objects.filter(username__iexact=username).exists():
            return render(
                request,
                "main/register_user.html",
                {
                    "error": "This username is already taken. Please choose another one.",
                    "username": username
                }
            )

        # -----------------------------
        # Password validation
        # -----------------------------

        if len(password) < 8:
            return render(
                request,
                "main/register_user.html",
                {
                    "error": "Password must contain at least 8 characters.",
                    "username": username
                }
            )

        if not re.search(r"[A-Z]", password):
            return render(
                request,
                "main/register_user.html",
                {
                    "error": "Password must contain at least one uppercase letter.",
                    "username": username
                }
            )

        if not re.search(r"[a-z]", password):
            return render(
                request,
                "main/register_user.html",
                {
                    "error": "Password must contain at least one lowercase letter.",
                    "username": username
                }
            )

        if not re.search(r"[0-9]", password):
            return render(
                request,
                "main/register_user.html",
                {
                    "error": "Password must contain at least one number.",
                    "username": username
                }
            )

        if not re.search(r"[^A-Za-z0-9]", password):
            return render(
                request,
                "main/register_user.html",
                {
                    "error": "Password must contain at least one special character.",
                    "username": username
                }
            )

        # -----------------------------
        # Confirm password
        # -----------------------------

        if password != password2:
            return render(
                request,
                "main/register_user.html",
                {
                    "error": "Passwords do not match.",
                    "username": username
                }
            )

        # -----------------------------
        # Create user
        # -----------------------------

        try:

            user = User.objects.create_user(
                username=username,
                password=password
            )

            # Automatically log in after registration
            login(request, user)

            return redirect("index")

        except Exception as e:

            print(f"Registration error: {e}")

            return render(
                request,
                "main/register_user.html",
                {
                    "error": "Something went wrong while creating your account.",
                    "username": username
                }
            )

    return render(request, "main/register_user.html")


# ============================================================
# LOGIN USER
# ============================================================

# Login user
def login_user(request):

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        if not username or not password:

            return render(
                request,
                "main/login_user.html",
                {
                    "error": "Please enter both username and password.",
                    "username": username
                }
            )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("index")

        else:

            return render(
                request,
                "main/login_user.html",
                {
                    "error": "Invalid username or password.",
                    "username": username
                }
            )

    return render(request, "main/login_user.html")


# ============================================================
# LOGOUT USER
# ============================================================

def logout_user(request):

    logout(request)

    print(
        "Successfully logged out!!!"
    )

    return redirect(
        'index'
    )



# ============================================================
# USER PROFILE
# ============================================================

@login_required
def profile(request):

    # Get or create the profile for the logged-in user
    user_profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    # Profile statistics
    song_count = Song.objects.count()

    liked_count = request.user.liked_songs.count()

    playlist_count = Playlist.objects.filter(
        user=request.user
    ).count()

    return render(
        request,
        'main/profile.html',
        {
            'user_profile': user_profile,
            'song_count': song_count,
            'liked_count': liked_count,
            'playlist_count': playlist_count,
        }
    )

@login_required
def delete_playlist(request, pk):

    if request.method != "POST":
        return redirect("all_playlists")

    playlist = get_object_or_404(
        Playlist,
        id=pk
    )

    # --------------------------------------------------------
    # FEATURED PLAYLIST
    # Only admin can delete a featured playlist.
    # --------------------------------------------------------
    if playlist.is_featured:

        if not request.user.is_superuser:
            return redirect(
                "view_playlist",
                pk=playlist.pk
            )

    # --------------------------------------------------------
    # NORMAL PLAYLIST
    # Only the owner can delete it.
    # --------------------------------------------------------
    else:

        if playlist.user != request.user:
            return redirect(
                "view_playlist",
                pk=playlist.pk
            )

    playlist_name = playlist.name

    playlist.delete()

    messages.success(
        request,
        f'Playlist "{playlist_name}" was deleted successfully.'
    )

    return redirect("all_playlists")

# ============================================================
# SETTINGS
# ============================================================

@login_required
def settings_page(request):

    return render(
        request,
        'main/settings.html'
    )


# ============================================================
# DELETE ACCOUNT
# ============================================================

@login_required
def delete_account(request):

    if request.method == "POST":

        user = request.user

        # Keep the profile picture reference before deleting the user
        profile_picture = None

        if hasattr(user, "profile") and user.profile.profile_picture:
            profile_picture = user.profile.profile_picture

        with transaction.atomic():

            # Delete the user.
            #
            # This automatically deletes:
            # - UserProfile
            # - User's Playlists
            # - User's liked-song relationships
            #
            # It DOES NOT delete Song objects.
            user.delete()

        # Delete the physical profile picture file
        if profile_picture:
            profile_picture.delete(save=False)

        logout(request)

        return redirect("login_user")

    return redirect("settings")


# ============================================================
# CHANGE PROFILE PICTURE
# ============================================================

@login_required
def change_profile_picture(request):

    if request.method == "POST":

        user_profile, created = UserProfile.objects.get_or_create(
            user=request.user
        )

        profile_picture = request.FILES.get("profile_picture")

        if profile_picture:

            # Delete old picture from storage
            if user_profile.profile_picture:
                user_profile.profile_picture.delete(save=False)

            # Save new picture
            user_profile.profile_picture = profile_picture
            user_profile.save()

            messages.success(
                request,
                "Profile picture updated successfully."
            )

        return redirect("profile")

    return redirect("profile")


# ============================================================
# REMOVE PROFILE PICTURE
# ============================================================

@login_required
def remove_profile_picture(request):

    if request.method == "POST":

        user_profile, created = UserProfile.objects.get_or_create(
            user=request.user
        )

        if user_profile.profile_picture:

            user_profile.profile_picture.delete(save=False)
            user_profile.profile_picture = None
            user_profile.save()

            messages.success(
                request,
                "Profile picture removed successfully."
            )

        return redirect("profile")

    return redirect("profile")


# ============================================================
# CREATE PLAYLIST
# ============================================================

def create_playlist(request):

    if request.method == "POST":

        name_playlist = request.POST.get(
            "name-playlist"
        )

        if request.user.is_authenticated:

            playlist = Playlist.objects.create(
                name=name_playlist,
                user=request.user
            )

            playlist.save()

            return redirect(
                "index"
            )

        else:

            return redirect(
                'index'
            )

    return render(
        request,
        'main/create_playlist.html'
    )






# ============================================================
# VIEW PLAYLIST
# ============================================================

def view_playlist(request, pk):

    if not request.user.is_authenticated:
        return redirect(
            'index'
        )

    # --------------------------------------------------------
    # Playlist access
    #
    # Users can open:
    # 1. Their own playlists
    # 2. Featured playlists created/managed by admin
    #
    # Featured playlists are read-only in the normal app.
    # --------------------------------------------------------

    playlist = get_object_or_404(
        Playlist,
        Q(id=pk) & (
            Q(user=request.user) |
            Q(is_featured=True)
        )
    )

    # --------------------------------------------------------
    # Remove a song
    #
    # Only the owner of a normal playlist can remove songs.
    # Featured playlists cannot be modified from the app.
    # --------------------------------------------------------

    if request.method == "POST":

        # Featured playlists are completely read-only
            # inside the normal application.
            # They are managed only from Django Admin.

        if playlist.is_featured:
            if not request.user.is_superuser:
                return redirect(
                    'view_playlist',
                    pk=playlist.pk
                )
                
        
            # Normal playlist:
            # only its owner can modify it.
        else:

            if playlist.user != request.user:
                return redirect(
                    'view_playlist',
                    pk=playlist.pk
                )
        
        remove_song_id = request.POST.get("remove_song_id")
        
        if remove_song_id:
        
            song = get_object_or_404(
                    Song,
                    id=remove_song_id
                )
        
            if playlist.song.filter(
                    pk=song.pk
                ).exists():
        
                playlist.song.remove(song)
        
                messages.success(
                        request,
                        f'Removed "{song.title}" from "{playlist.name}".'
                    )
        
        return redirect(
                'view_playlist',
                pk=playlist.pk
            )

    
    

    # --------------------------------------------------------
    # Player
    # --------------------------------------------------------

    play_song_id = request.GET.get(
        'play'
    )

    shuffle = (
        request.GET.get(
            'shuffle',
            'false'
        ) == 'true'
    )

    play_song = None
    previous_song = None
    next_song = None
    shuffle_song = None
    upcoming_songs = []
    youtube_queue = []

    # --------------------------------------------------------
    # Playlist songs
    # --------------------------------------------------------

    playlist_list = list(
        playlist.song.all()
    )

    # --------------------------------------------------------
    # Current song
    # --------------------------------------------------------

    if play_song_id:

        play_song = get_object_or_404(
            Song,
            id=play_song_id
        )

        # Make sure the song belongs to this playlist.
        if play_song not in playlist_list:

            play_song = None

    # --------------------------------------------------------
    # Playlist navigation
    # --------------------------------------------------------

    if play_song and playlist_list:

        current_index = playlist_list.index(
            play_song
        )

        upcoming_songs = (
            playlist_list[current_index + 1:]
            + playlist_list[:current_index]
        )

        if shuffle:

            random_shuffle(
                upcoming_songs
            )

        youtube_queue = [
            play_song
        ] + upcoming_songs

        # Previous
        if current_index > 0:

            previous_song = playlist_list[
                current_index - 1
            ]

        else:

            previous_song = playlist_list[-1]

        # Next
        if current_index < len(playlist_list) - 1:

            next_song = playlist_list[
                current_index + 1
            ]

        else:

            next_song = playlist_list[0]

        # Shuffle
        possible_songs = [
            song
            for song in playlist_list
            if song != play_song
        ]

        if possible_songs:

            shuffle_song = choice(
                possible_songs
            )

    user_playlists = Playlist.objects.filter(
    user=request.user
)

    # --------------------------------------------------------
    # Render playlist
    # --------------------------------------------------------

    return render(
        request,
        'main/view_playlist.html',
        {
            'playlist': playlist,
            'playlist_songs': playlist_list,
            'playlists': user_playlists,
            'next_song': next_song,
            'previous_song': previous_song,
            'shuffle_song': shuffle_song,
            'play_song': play_song,
            'shuffle': shuffle,
            'upcoming_songs': upcoming_songs,
            'youtube_queue': youtube_queue,
        }
    )


# ============================================================
# ALL PLAYLISTS
# ============================================================

def all_playlists(request):

    if not request.user.is_authenticated:

        return redirect(
            'index'
        )

    playlists = Playlist.objects.filter(
        user=request.user
    )

    return render(
        request,
        'main/all_playlists.html',
        {
            'playlists': playlists
        }
    )