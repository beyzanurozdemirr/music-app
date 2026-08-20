from rest_framework import generics, permissions
from django.contrib.auth.models import User
from .serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    """Yeni kullanıcı kayıt endpoint'i."""
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)   # Giriş yapmamış herkes kayıt olabilsin
    serializer_class = RegisterSerializer