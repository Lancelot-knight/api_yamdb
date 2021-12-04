from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router_v1 = DefaultRouter()
router_v1.register('titles', views.TitleViewSet, basename='title')
router_v1.register('categories', views.CategoryViewSet, basename='category')
router_v1.register('genres', views.GenreViewSet, basename='genre')
router_v1.register('users', views.UserViewSet, basename='users')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', views.SignupView.as_view(), name="signup"),
    path('v1/auth/token/', views.RefreshTokenView.as_view(), name="token")
]
