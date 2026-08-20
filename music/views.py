from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Artist, Album, Song, Playlist, Favorite
from .serializers import (
    ArtistSerializer, AlbumSerializer, SongSerializer,
    PlaylistSerializer, FavoriteSerializer
)


class ArtistViewSet(viewsets.ModelViewSet):
    """Sanatçılar için CRUD (listele/getir/oluştur/güncelle/sil) işlemleri."""
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class AlbumViewSet(viewsets.ModelViewSet):
    """Albümler için CRUD işlemleri."""
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['artist']
    search_fields = ['title']
class SongViewSet(viewsets.ModelViewSet):
    """Şarkılar için CRUD işlemleri + arama."""
    queryset = Song.objects.all().order_by('order')
    serializer_class = SongSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['artist', 'album']
    search_fields = ['title', 'artist__name', 'album__title']
class PlaylistViewSet(viewsets.ModelViewSet):
    """Kullanıcının kendi çalma listeleri için CRUD işlemleri."""
    serializer_class = PlaylistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Sadece giriş yapmış kullanıcının kendi playlist'lerini döndür
        return Playlist.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Yeni playlist oluşturulurken 'user' alanını otomatik olarak giriş yapan kullanıcı yap
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def add_song(self, request, pk=None):
        """Playlist'e şarkı ekleme. Örnek kullanım: POST /api/playlists/1/add_song/
        Body: {"song_id": 3}"""
        playlist = self.get_object()
        song_id = request.data.get('song_id')
        try:
            song = Song.objects.get(id=song_id)
        except Song.DoesNotExist:
            return Response({'error': 'Şarkı bulunamadı.'}, status=404)
        playlist.songs.add(song)
        return Response({'status': 'şarkı eklendi', 'song': song.title})

    @action(detail=True, methods=['post'])
    def remove_song(self, request, pk=None):
        """Playlist'ten şarkı çıkarma. Örnek kullanım: POST /api/playlists/1/remove_song/
        Body: {"song_id": 3}"""
        playlist = self.get_object()
        song_id = request.data.get('song_id')
        try:
            song = Song.objects.get(id=song_id)
        except Song.DoesNotExist:
            return Response({'error': 'Şarkı bulunamadı.'}, status=404)
        playlist.songs.remove(song)
        return Response({'status': 'şarkı çıkarıldı', 'song': song.title})
class FavoriteViewSet(viewsets.ModelViewSet):
    """Kullanıcının favori şarkıları için işlemler."""
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)