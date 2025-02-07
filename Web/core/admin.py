from django.contrib import admin
from .models import Profile,Notification, CareerPreference, JobTitle, Location

class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "location", "created_at", "updated_at")
    search_fields = ("user__email", "user__first_name", "user__last_name", "location")
    list_filter = ("created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")

class CareerPreferenceAdmin(admin.ModelAdmin):
    list_display = ("user", "work_type", "industry", "education_level")
    search_fields = ("user__email", "user__first_name", "user__last_name", "industry")
    list_filter = ("work_type", "education_level")

class JobTitleAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)

class LocationAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "notification_type", "sent_date", "read_status")
    search_fields = ("user__email", "notification_type")
    list_filter = ("sent_date", "read_status")

admin.site.register(Profile, ProfileAdmin)
admin.site.register(CareerPreference, CareerPreferenceAdmin)
admin.site.register(JobTitle, JobTitleAdmin)
admin.site.register(Location, LocationAdmin)

admin.site.register(Notification, NotificationAdmin)