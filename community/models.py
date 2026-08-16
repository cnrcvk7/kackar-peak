from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class ActivityType(models.TextChoices):
    RUN = "run", "Koşu"
    YOGA = "yoga", "Yoga & Pilates"
    HIKE = "hike", "Doğa Yürüyüşü"
    BIKE = "bike", "Bisiklet"


class Event(models.Model):
    """A single scheduled community event (run, yoga session, hike)."""
    title = models.CharField("Başlık", max_length=200)
    activity_type = models.CharField(
        "Aktivite türü", max_length=20,
        choices=ActivityType.choices, default=ActivityType.RUN,
    )
    description = models.TextField("Açıklama", blank=True)
    location = models.CharField("Buluşma noktası", max_length=200)
    start_time = models.DateTimeField("Başlangıç zamanı")
    distance_km = models.DecimalField(
        "Mesafe (km)", max_digits=5, decimal_places=1,
        null=True, blank=True,
    )
    level = models.CharField(
        "Seviye", max_length=100, blank=True,
        help_text="ör. Tüm seviyeler, Orta, İleri",
    )
    coffee_note = models.CharField(
        "Kahve ikramı", max_length=200, blank=True,
        help_text="ör. Etkinlik sonrası V60 demleme ikramı",
    )
    participant_count = models.PositiveIntegerField("Katılımcı sayısı", default=0)
    is_weekly = models.BooleanField("Haftalık tekrar", default=False)
    is_published = models.BooleanField("Yayında", default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["start_time"]
        verbose_name = "Etkinlik"
        verbose_name_plural = "Etkinlikler"

    def __str__(self):
        return f"{self.title} — {self.start_time:%d.%m.%Y %H:%M}"

    @property
    def is_upcoming(self):
        return self.start_time >= timezone.now()

    @property
    def badge_class(self):
        return {"run": "b-run", "yoga": "b-yoga", "hike": "b-hike",
                "bike": "b-bike"}.get(self.activity_type, "b-run")


class Activity(models.Model):
    """One of the activity categories shown on the home page."""
    title = models.CharField("Başlık", max_length=100)
    subtitle = models.CharField("Alt başlık", max_length=200, blank=True)
    description = models.TextField("Açıklama")
    order = models.PositiveIntegerField("Sıra", default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Aktivite"
        verbose_name_plural = "Aktiviteler"

    def __str__(self):
        return self.title


class FAQ(models.Model):
    question = models.CharField("Soru", max_length=300)
    answer = models.TextField("Cevap")
    order = models.PositiveIntegerField("Sıra", default=0)
    is_published = models.BooleanField("Yayında", default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "SSS"
        verbose_name_plural = "SSS"

    def __str__(self):
        return self.question


class GalleryImage(models.Model):
    image = models.ImageField("Görsel", upload_to="gallery/")
    caption = models.CharField("Başlık", max_length=200, blank=True)
    event = models.ForeignKey(
        Event, null=True, blank=True,
        on_delete=models.SET_NULL, related_name="photos",
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]
        verbose_name = "Galeri görseli"
        verbose_name_plural = "Galeri"

    def __str__(self):
        return self.caption or f"Görsel #{self.pk}"


class SiteStat(models.Model):
    """Editable stats shown in the 'about' section."""
    number = models.CharField("Rakam", max_length=20, help_text="ör. 200+")
    key = models.CharField("Etiket", max_length=60, help_text="ör. Topluluk")
    text = models.CharField("Açıklama", max_length=200)
    order = models.PositiveIntegerField("Sıra", default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "İstatistik"
        verbose_name_plural = "İstatistikler"

    def __str__(self):
        return f"{self.number} {self.key}"


# ---------------------------------------------------------------------------
# User community features: profile, RSVP, gallery comments & likes
# ---------------------------------------------------------------------------

class Profile(models.Model):
    """Extra info attached to each user account. Created automatically on signup."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField("Profil fotoğrafı", upload_to="avatars/", blank=True)
    bio = models.CharField("Hakkında", max_length=280, blank=True)
    favorite_coffee = models.CharField(
        "Favori kahve / demleme", max_length=120, blank=True,
        help_text="ör. V60, Chemex, Türk kahvesi",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profiller"

    def __str__(self):
        return f"{self.user.username} profili"

    @property
    def events_attended(self):
        """Live count of events this user has RSVP'd to — never stored, always current."""
        return self.user.rsvps.count()


class RSVP(models.Model):
    """A user's commitment to attend an event. One per user per event."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rsvps")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="rsvps")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "event")
        verbose_name = "Katılım"
        verbose_name_plural = "Katılımlar"

    def __str__(self):
        return f"{self.user.username} → {self.event.title}"


class Comment(models.Model):
    """A comment on a gallery image. Hidden until approved by an admin."""
    image = models.ForeignKey(
        GalleryImage, on_delete=models.CASCADE, related_name="comments",
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField("Yorum", max_length=1000)
    is_approved = models.BooleanField(
        "Onaylandı", default=False,
        help_text="İşaretlenene kadar yorum sitede görünmez.",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Yorum"
        verbose_name_plural = "Yorumlar"

    def __str__(self):
        return f"{self.author.username}: {self.text[:40]}"

    @property
    def like_count(self):
        return self.likes.count()


class CommentLike(models.Model):
    """One like per user per comment."""
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("comment", "user")
        verbose_name = "Yorum beğenisi"
        verbose_name_plural = "Yorum beğenileri"

    def __str__(self):
        return f"{self.user.username} ♥ {self.comment_id}"
