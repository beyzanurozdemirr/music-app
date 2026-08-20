from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Artist(models.Model):
    """Sanatçı bilgilerini tutan model."""
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='artists/', blank=True, null=True)

    def __str__(self):
        return self.name


class Album(models.Model):
    """Albüm bilgilerini tutan model."""
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums')
    cover_image = models.ImageField(upload_to='albums/', blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.artist.name}"


class Song(models.Model):
    """Şarkı bilgilerini tutan model."""
    title = models.CharField(max_length=200)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='songs', blank=True, null=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='songs')
    duration = models.PositiveIntegerField(help_text='Saniye cinsinden süre')
    audio_file = models.FileField(upload_to='songs/')
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class Playlist(models.Model):
    """Kullanıcıların oluşturduğu çalma listesi."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists')
    name = models.CharField(max_length=200)
    songs = models.ManyToManyField(Song, related_name='playlists', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Favorite(models.Model):
    """Kullanıcının beğendiği (favori) şarkılar."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='favorited_by')

    class Meta:
        unique_together = ('user', 'song')  # Aynı şarkı bir kullanıcı tarafından 2 kez favorilenemesin

    def __str__(self):
        return f"{self.user.username} - {self.song.title}"