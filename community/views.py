from django.shortcuts import render
from django.utils import timezone
from .models import Event, Activity, FAQ, GalleryImage, SiteStat


def home(request):
    now = timezone.now()
    upcoming = Event.objects.filter(
        is_published=True, start_time__gte=now
    ).order_by("start_time")[:6]
    context = {
        "upcoming_events": upcoming,
        "activities": Activity.objects.all(),
        "faqs": FAQ.objects.filter(is_published=True),
        "stats": SiteStat.objects.all(),
    }
    return render(request, "community/home.html", context)


def events(request):
    now = timezone.now()
    upcoming = Event.objects.filter(
        is_published=True, start_time__gte=now
    ).order_by("start_time")
    past = Event.objects.filter(
        is_published=True, start_time__lt=now
    ).order_by("-start_time")[:12]
    return render(request, "community/events.html", {
        "upcoming_events": upcoming,
        "past_events": past,
    })


def gallery(request):
    return render(request, "community/gallery.html", {
        "images": GalleryImage.objects.select_related("event").all(),
    })
