from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),   # root URL
    path("polish/", views.polish_draft, name="polish"),
    path("history/", views.history, name="history"),
    path("delete-draft/<int:id>/", views.delete_draft, name="delete_draft"),
]