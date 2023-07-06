from django.urls import path
from .views import leaderboard_view, leaderboard_update_api, add_lap_score
from django.contrib.auth.views import LoginView

app_name = "leaderboard_app"

urlpatterns = [
    path('', leaderboard_view, name='leaderboard'),
    path('api/leaderboard/', leaderboard_update_api, name='leaderboard_update_api'),
    path("add_lap_score/", add_lap_score, name="add_lap_score"),
    path("login/", LoginView.as_view(template_name="leaderboard_app/login.html"), name="login"),
]