from django.contrib import admin
from .models import Event, Activity, FAQ, GalleryImage, SiteStat


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "activity_type", "start_time", "location",
                    "participant_count", "is_weekly", "is_published")
    list_filter = ("activity_type", "is_weekly", "is_published")
    search_fields = ("title", "location", "description")
    list_editable = ("participant_count", "is_published")
    date_hierarchy = "start_time"
    fieldsets = (
        (None, {"fields": ("title", "activity_type", "description")}),
        ("Zaman & Yer", {"fields": ("start_time", "location", "distance_km", "level")}),
        ("Kahve", {"fields": ("coffee_note",), "description": "Etkinlik sonrası ikram edilecek kahve"}),
        ("Ayarlar", {"fields": ("participant_count", "is_weekly", "is_published")}),
    )


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("title", "subtitle", "order")
    list_editable = ("order",)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "order", "is_published")
    list_editable = ("order", "is_published")


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ("__str__", "event", "uploaded_at")
    list_filter = ("event",)


@admin.register(SiteStat)
class SiteStatAdmin(admin.ModelAdmin):
    list_display = ("number", "key", "text", "order")
    list_editable = ("order",)


from .models import Profile, RSVP, Comment, CommentLike


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "favorite_coffee", "events_attended", "created_at")
    search_fields = ("user__username", "favorite_coffee")


@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    list_display = ("user", "event", "created_at")
    list_filter = ("event",)
    search_fields = ("user__username", "event__title")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "image", "short_text", "is_approved", "like_count", "created_at")
    list_filter = ("is_approved", "created_at")
    list_editable = ("is_approved",)
    search_fields = ("author__username", "text")
    actions = ["approve_comments"]

    @admin.display(description="Yorum")
    def short_text(self, obj):
        return obj.text[:60]

    @admin.action(description="Seçili yorumları onayla")
    def approve_comments(self, request, queryset):
        n = queryset.update(is_approved=True)
        self.message_user(request, f"{n} yorum onaylandı.")


@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ("user", "comment", "created_at")
