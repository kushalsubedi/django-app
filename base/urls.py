from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("", views.home, name="home"),
    path("room/<str:pk>/", views.room, name="room"),
    path("create_room/", views.createRoom, name="create_room"),
    path("update/<str:pk>/", views.updateRoom, name="update"),
    path("delete/<str:pk>/", views.deleteRoom, name="delete"),
]
