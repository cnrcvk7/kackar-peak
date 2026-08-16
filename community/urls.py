from django.urls import path
from . import views

app_name = "community"

urlpatterns = [
    path("", views.home, name="home"),
    path("etkinlikler/", views.events, name="events"),
    path("galeri/", views.gallery, name="gallery"),

    # profile & auth
    path("kayit/", views.signup, name="signup"),
    path("profil/", views.profile, name="profile"),

    # actions
    path("etkinlik/<int:event_id>/katil/", views.toggle_rsvp, name="toggle_rsvp"),
    path("galeri/<int:image_id>/yorum/", views.post_comment, name="post_comment"),
    path("yorum/<int:comment_id>/begen/", views.toggle_like, name="toggle_like"),
]
