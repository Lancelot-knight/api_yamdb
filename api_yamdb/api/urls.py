from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router_v1 = DefaultRouter()
router_v1.register('titles', views.TitleViewSet, basename='title')
router_v1.register('categories', views.CategoryViewSet, basename='category')
router_v1.register('genres', views.GenreViewSet, basename='genre')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]