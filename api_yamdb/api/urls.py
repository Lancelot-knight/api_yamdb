from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router_v1 = DefaultRouter()
router_v1.register(
    r'titles/(?P<title_id>[^/.]+)/reviews', views.ReviewViewSet, basename='review'
)
router_v1.register(
    r'titles/(?P<title_id>[^/.]+)/reviews/(?P<review_id>[^/.]+)/comments', views.CommentViewSet, basename='comments'
)
urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
