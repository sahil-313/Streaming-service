from django.urls import path
from . import views

urlpatterns = [
    # Example: path('route/', views.view_function, name='route_name'),
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("signup", views.signup, name="signup"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("upload", views.upload_video, name="upload_video"),
    path("watch/<int:video_id>", views.watch_video, name="watch_video"),
    path("comment/<int:video_id>", views.comment, name="comment"),
    path("new_playlist", views.new_playlist, name="new_playlist"),
    path("playlist/<str:playlist>", views.playlist_content, name="playlist"),
    path("edit_profile", views.edit_profile, name="edit_profile"),
    path("search_videos", views.search_videos, name="search_videos"),

    # API routes
    path("get_videos", views.get_videos, name="get_videos"),
    path("action/<str:action>/<int:video_id>", views.action, name="action"),
    path("user_videos/<int:user_id>/<str:type>", views.user_videos, name="user_videos"),
    path("sub_or_unsub/<int:user_id>/<str:action>", views.sub_or_unsub, name="sub_or_unsub"),
    path("subscriptions_videos", views.subscriptions_videos, name="subscriptions_videos"),
    path("get_user_playlists", views.get_user_playlists, name="get_user_playlists"),
    path("add_to_playlist/<str:playlist>/<int:video_id>", views.add_to_playlist, name="add_to_playlist"),
    path("playlist_content/<str:playlist>", views.playlist_content, name="playlist_content")
]
