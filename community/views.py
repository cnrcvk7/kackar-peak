from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import (
    Event, Activity, FAQ, GalleryImage, SiteStat,
    RSVP, Comment, CommentLike,
)
from .forms import SignUpForm, ProfileForm, CommentForm


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

    # Which of these events has the current user already joined?
    joined_ids = set()
    if request.user.is_authenticated:
        joined_ids = set(
            request.user.rsvps.values_list("event_id", flat=True)
        )

    return render(request, "community/events.html", {
        "upcoming_events": upcoming,
        "past_events": past,
        "joined_ids": joined_ids,
    })


def gallery(request):
    images = GalleryImage.objects.select_related("event").prefetch_related(
        "comments__author", "comments__likes"
    ).all()

    liked_ids = set()
    if request.user.is_authenticated:
        liked_ids = set(
            request.user.comment_likes.values_list("comment_id", flat=True)
        )

    return render(request, "community/gallery.html", {
        "images": images,
        "comment_form": CommentForm(),
        "liked_ids": liked_ids,
    })


# ---------------------------------------------------------------------------
# Auth & profile
# ---------------------------------------------------------------------------

def signup(request):
    if request.user.is_authenticated:
        return redirect("community:profile")
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            if form.cleaned_data.get("email"):
                user.email = form.cleaned_data["email"]
                user.save()
            login(request, user)
            messages.success(request, "Hoş geldin! Profilini tamamlayabilirsin.")
            return redirect("community:profile")
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form})


@login_required
def profile(request):
    prof = request.user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=prof)
        if form.is_valid():
            form.save()
            messages.success(request, "Profilin güncellendi.")
            return redirect("community:profile")
    else:
        form = ProfileForm(instance=prof)

    my_events = Event.objects.filter(
        rsvps__user=request.user
    ).order_by("start_time")

    return render(request, "community/profile.html", {
        "form": form,
        "profile": prof,
        "my_events": my_events,
    })


# ---------------------------------------------------------------------------
# Actions (POST only)
# ---------------------------------------------------------------------------

@login_required
@require_POST
def toggle_rsvp(request, event_id):
    event = get_object_or_404(Event, pk=event_id, is_published=True)
    rsvp, created = RSVP.objects.get_or_create(user=request.user, event=event)
    if not created:
        rsvp.delete()
        messages.info(request, f"“{event.title}” katılımın iptal edildi.")
    else:
        messages.success(request, f"“{event.title}” etkinliğine katılıyorsun!")
    return redirect(request.META.get("HTTP_REFERER", "community:events"))


@login_required
@require_POST
def post_comment(request, image_id):
    image = get_object_or_404(GalleryImage, pk=image_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.image = image
        comment.author = request.user
        comment.save()
        messages.success(
            request,
            "Yorumun alındı — onaylandıktan sonra yayınlanacak.",
        )
    return redirect("community:gallery")


@login_required
@require_POST
def toggle_like(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, is_approved=True)
    like, created = CommentLike.objects.get_or_create(
        comment=comment, user=request.user
    )
    if not created:
        like.delete()
    return redirect("community:gallery")
