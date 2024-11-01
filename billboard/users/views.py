from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination

from .models import User
from .permissions import CreateOnlyOrSuperuserPermission
from .serializers import UserSerializer


class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (CreateOnlyOrSuperuserPermission,)
