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

    # API routes
    path("get_videos", views.get_videos, name="get_videos")
]
