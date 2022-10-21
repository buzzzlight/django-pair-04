from django.urls import path
from . import views

app_name = "mailing"

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("<int:pk>/", views.detail, name="detail"),
    path("sent/", views.sent, name="sent"),
    path("bin/", views.bin, name="bin"),
    path("important/", views.important, name="important"),
    path("<int:pk>/delete/", views.delete, name="delete"),
    path("<int:pk>/trash_throw_away/", views.trash_throw_away, name="trash_throw_away"),
    path("<int:pk>/trash_return/", views.trash_return, name="trash_return"),
    path("<int:pk>/important_check/", views.important_check, name="important_check"),
    path("<int:pk>/important_return/", views.important_return, name="important_return"),
]