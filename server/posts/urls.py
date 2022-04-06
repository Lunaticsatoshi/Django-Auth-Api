from django.urls import path
from .views import UserPostListApiView, UserPostCreateApiView, UserPostUpdateApiView, UserPostDetailApiView, UserPostDeleteApiView, get_post, get_posts, get_comments, add_comment

urlpatterns = [
    path('user/all/', UserPostListApiView.as_view(), name='user-post-list'),
    path('user/<str:id>/', UserPostDetailApiView.as_view(), name='user-post-detail'),
    path('create/', UserPostCreateApiView.as_view(), name='user-post-create'),
    path('<str:id>/update/', UserPostUpdateApiView.as_view(), name='user-post-update'),
    path('<str:id>/delete/', UserPostDeleteApiView.as_view(), name='user-post-delete'),
    path('all/', get_posts, name='all-posts'),
    path('<str:slug>/comment/', get_comments, name='post-comments'),
    path('comment/', add_comment, name='add-comment'),
    path('<str:slug>/', get_post, name='post-detail'),
]