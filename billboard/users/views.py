from rest_framework import generics

from .models import User
from .permissions import CreateOnlyOrSuperuserPermission
from .serializers import UserSerializer


class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (CreateOnlyOrSuperuserPermission,)
