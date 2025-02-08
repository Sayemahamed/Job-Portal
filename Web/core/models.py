from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import os

# Create your models here.


class Profile(models.Model):
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
        ("N", "Prefer not to say"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default="N")
    location = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email}'s Profile"

    def save(self, *args, **kwargs):
        # If this is an update and we have a new avatar
        if self.pk:
            try:
                old_profile = Profile.objects.get(pk=self.pk)
                if old_profile.avatar and old_profile.avatar != self.avatar:
                    # Delete the old avatar file
                    if os.path.exists(old_profile.avatar.path):
                        os.remove(old_profile.avatar.path)
            except Profile.DoesNotExist:
                pass

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a Profile instance whenever a new User is created."""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Ensure the Profile is saved whenever the User is saved."""
    instance.profile.save()


class CareerPreference(models.Model):
    WORK_TYPE_CHOICES = [
        ("Remote", "Remote"),
        ("Hybrid", "Hybrid"),
        ("Onsite", "On-site"),
    ]
    EDUCATION_LEVEL_CHOICES = [
        ("HS", "High School"),
        ("BA", "Bachelor"),
        ("MA", "Master"),
        ("PhD", "PhD"),
    ]
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="career_preference"
    )
    min_salary = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    max_salary = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    work_type = models.CharField(
        max_length=10, choices=WORK_TYPE_CHOICES, default="Onsite"
    )
    industry = models.CharField(max_length=100, blank=True)
    years_of_experience = models.PositiveIntegerField(null=True, blank=True)
    education_level = models.CharField(
        max_length=3, choices=EDUCATION_LEVEL_CHOICES, blank=True
    )
    # Using ManyToMany to junction tables for preferred job titles and locations:
    preferred_job_titles = models.ManyToManyField(
        "JobTitle", blank=True, related_name="preferred_by"
    )
    preferred_locations = models.ManyToManyField(
        "Location", blank=True, related_name="preferred_by"
    )

    def __str__(self):
        return f"Career Preferences for {self.user.email}"


class JobTitle(models.Model):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title


class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Notification(models.Model):
    NOTIFICATION_TYPE_CHOICES = [
        ("Job Alert", "Job Alert"),
        ("Market Trend", "Market Trend"),
        ("Resource", "Resource"),
    ]
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )
    notification_type = models.CharField(
        max_length=50, choices=NOTIFICATION_TYPE_CHOICES
    )
    content = models.TextField()
    sent_date = models.DateTimeField(auto_now_add=True)
    read_status = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.email}: {self.notification_type}"
