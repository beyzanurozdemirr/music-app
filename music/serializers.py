from rest_framework import serializers
from .models import Artist, Album, Song, Playlist, Favorite


class ArtistSerializer(serializers.ModelSerializer):
    """Sanatçı verisini JSON'a çeviren serializer."""

    class Meta:
        model = Artist
        fields = ['id', 'name', 'bio', 'image']


class AlbumSerializer(serializers.ModelSerializer):
    """Albüm verisini JSON'a çeviren serializer.
    artist_name alanı, ilişkili sanatçının ismini de göstermek için eklendi."""
    artist_name = serializers.CharField(source='artist.name', read_only=True)

    class Meta:
        model = Album
        fields = ['id', 'title', 'artist', 'artist_name', 'cover_image', 'release_date']


class SongSerializer(serializers.ModelSerializer):
    """Şarkı verisini JSON'a çeviren serializer.
    artist_name ve album_title alanları, ilişkili verileri de göstermek için eklendi."""
    artist_name = serializers.CharField(source='artist.name', read_only=True)
    album_title = serializers.CharField(source='album.title', read_only=True, default=None)

    class Meta:
        model = Song
        fields = ['id', 'title', 'artist', 'artist_name', 'album', 'album_title',
                   'duration', 'audio_file', 'order']


class PlaylistSerializer(serializers.ModelSerializer):
    """Çalma listesi verisini JSON'a çeviren serializer.
    songs alanında, playlist'teki şarkıların detaylarını (sadece okuma için) gösteriyoruz."""
    songs = SongSerializer(many=True, read_only=True)
    song_count = serializers.IntegerField(source='songs.count', read_only=True)

    class Meta:
        model = Playlist
        fields = ['id', 'name', 'user', 'songs', 'song_count', 'created_at']
        read_only_fields = ['user']


class FavoriteSerializer(serializers.ModelSerializer):
    """Favori şarkı verisini JSON'a çeviren serializer."""
    song = SongSerializer(read_only=True)
    song_id = serializers.PrimaryKeyRelatedField(
        queryset=Song.objects.all(), source='song', write_only=True
    )

    class Meta:
        model = Favorite
        fields = ['id', 'song', 'song_id']