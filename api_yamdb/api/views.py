from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets, generics, status, permissions
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from reviews.models import Category, Genre, Title, User
from .filters import TitleFilter
from .permissions import IsAdminUserOrReadOnly, AdminOrSuperUserOnly
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleReadSerializer, TitleWriteSerializer,
    SignupSerializer, ConfirmationSerializer,
    UserSerializer, UserMeSerializer,
)


class SignupView(generics.GenericAPIView):
    serializer_class = SignupSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        email_body = f'Confirmation code: {user.confirmation_code}!'
        send_mail(
            'Confirmation code', email_body, 'root@mail.ru', (user.email,)
        )
        return Response(user_data, status=status.HTTP_200_OK)


class RefreshTokenView(generics.GenericAPIView):
    serializer_class = ConfirmationSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.data
        user = get_object_or_404(User, username=user_data['username'])
        if user.confirmation_code != user_data['confirmation_code']:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {'token': str(user.token)}, status=status.HTTP_200_OK
        )


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (AdminOrSuperUserOnly,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=[IsAuthenticated],
        serializer_class=UserMeSerializer
    )
    def me(self, request):
        self.kwargs['username'] = request.user.username
        user = get_object_or_404(User, pk=request.user.id)
        if self.request.method == 'PATCH':
            self.partial_update(request)
            patched_user = User.objects.get(pk=request.user.id)
            serializer = self.get_serializer(patched_user)
        else:
            serializer = self.get_serializer(user)
        return Response(serializer.data)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return TitleWriteSerializer
        return TitleReadSerializer


class MixinSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    pass


class CategoryViewSet(MixinSet):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']
    lookup_field = 'slug'


class GenreViewSet(MixinSet):
    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    pass


class CommentViewSet(viewsets.ModelViewSet):
    pass
