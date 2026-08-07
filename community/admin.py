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
