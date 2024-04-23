from django.urls import path
from . import views

urlpatterns = [
    # Example: path('route/', views.view_function, name='route_name'),
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("signup", views.signup, name="signup"),
    path("profile/<int:user_id>", views.profile, name="profile"),
]
