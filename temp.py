from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import (
    JSONField,
)  # Django 3.1+: use models.JSONField instead
from django.db.models.signals import post_save
from django.dispatch import receiver
import os

#############################################
# 1. User Profile and Career Preferences
#############################################


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
    # Additional career-related fields can be added here if desired.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email}'s Profile"

    def save(self, *args, **kwargs):
        # Remove old avatar file if updating avatar
        if self.pk:
            try:
                old_profile = Profile.objects.get(pk=self.pk)
                if old_profile.avatar and old_profile.avatar != self.avatar:
                    if os.path.exists(old_profile.avatar.path):
                        os.remove(old_profile.avatar.path)
            except Profile.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
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


#############################################
# 2. Resume and Resume Analysis
#############################################


class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="resumes")
    file = models.FileField(upload_to="resumes/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resume of {self.user.email} uploaded on {self.uploaded_at}"


class ResumeAnalysisResult(models.Model):
    resume = models.OneToOneField(
        Resume, on_delete=models.CASCADE, related_name="analysis"
    )
    experience_summary = models.TextField(blank=True)
    education_summary = models.TextField(blank=True)
    parsed_job_titles = models.TextField(blank=True)  # Can be a comma-separated list
    # Link to skills using a ManyToManyField
    skills = models.ManyToManyField("Skill", through="ResumeAnalysisSkill", blank=True)

    def __str__(self):
        return f"Analysis for {self.resume}"


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class ResumeAnalysisSkill(models.Model):
    analysis = models.ForeignKey(ResumeAnalysisResult, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("analysis", "skill")


#############################################
# 3. Job Postings, Companies, and Reviews
#############################################


class Company(models.Model):
    name = models.CharField(max_length=255)
    industry = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name


class JobPosting(models.Model):
    EMPLOYMENT_TYPE_CHOICES = [
        ("FT", "Full-time"),
        ("PT", "Part-time"),
        ("CT", "Contract"),
        ("IN", "Internship"),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="job_postings"
    )
    location = models.CharField(max_length=255)
    salary_range = models.CharField(max_length=50, blank=True)
    employment_type = models.CharField(
        max_length=2, choices=EMPLOYMENT_TYPE_CHOICES, default="FT"
    )
    posted_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField(null=True, blank=True)
    source = models.CharField(max_length=100, blank=True)  # e.g., LinkedIn, Indeed
    url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.title} at {self.company.name}"


class CompanyReview(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="reviews"
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.PositiveSmallIntegerField()  # 1-5 scale
    comment = models.TextField(blank=True)
    review_date = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=100, blank=True)  # e.g., Glassdoor

    def __str__(self):
        return f"Review for {self.company.name} by {self.user.email if self.user else 'Anonymous'}"


#############################################
# 4. Career Resources and User Interactions
#############################################


class CareerResource(models.Model):
    RESOURCE_TYPE_CHOICES = [
        ("Article", "Article"),
        ("Video", "Video"),
        ("Course", "Course"),
    ]
    title = models.CharField(max_length=255)
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPE_CHOICES)
    content = models.TextField(blank=True)  # or URL if linking externally
    published_date = models.DateField(null=True, blank=True)
    author = models.CharField(max_length=255, blank=True)
    source = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title


class UserResourceInteraction(models.Model):
    INTERACTION_TYPE_CHOICES = [
        ("View", "View"),
        ("Save", "Save"),
    ]
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="resource_interactions"
    )
    resource = models.ForeignKey(
        CareerResource, on_delete=models.CASCADE, related_name="interactions"
    )
    interaction_type = models.CharField(max_length=10, choices=INTERACTION_TYPE_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} {self.interaction_type} {self.resource.title}"


#############################################
# 5. Notifications, Job Matches, and Recommendations
#############################################


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
    # Optional related fields for context
    related_resource = models.ForeignKey(
        CareerResource, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"Notification for {self.user.email}: {self.notification_type}"


class JobMatch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="job_matches")
    job = models.ForeignKey(
        JobPosting, on_delete=models.CASCADE, related_name="matches"
    )
    match_score = models.FloatField()
    date_generated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Match for {self.user.email} with score {self.match_score}"


class ResourceRecommendation(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="resource_recommendations"
    )
    resource = models.ForeignKey(
        CareerResource, on_delete=models.CASCADE, related_name="recommendations"
    )
    score = models.FloatField()
    date_generated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resource Recommendation for {self.user.email} with score {self.score}"


#############################################
# 6. Applications and Coaching Sessions
#############################################


class Application(models.Model):
    APPLICATION_STATUS_CHOICES = [
        ("Applied", "Applied"),
        ("Interviewed", "Interviewed"),
        ("Rejected", "Rejected"),
    ]
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="applications"
    )
    job = models.ForeignKey(
        JobPosting, on_delete=models.CASCADE, related_name="applications"
    )
    application_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, choices=APPLICATION_STATUS_CHOICES, default="Applied"
    )
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.email} application for {self.job.title}"


class Coach(models.Model):
    name = models.CharField(max_length=255)
    specialty = models.CharField(max_length=255, blank=True)
    contact_info = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class CareerCoachingSession(models.Model):
    SESSION_STATUS_CHOICES = [
        ("Scheduled", "Scheduled"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="coaching_sessions"
    )
    coach = models.ForeignKey(
        Coach, on_delete=models.SET_NULL, null=True, blank=True, related_name="sessions"
    )
    scheduled_date = models.DateTimeField()
    duration = models.DurationField(null=True, blank=True)
    notes = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, choices=SESSION_STATUS_CHOICES, default="Scheduled"
    )

    def __str__(self):
        return f"Coaching Session for {self.user.email} on {self.scheduled_date}"


#############################################
# 7. Market Trends and User Job Alerts
#############################################


class MarketTrend(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    industry = models.CharField(max_length=100, blank=True)
    date_published = models.DateField(auto_now_add=True)
    source = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title


class UserJobAlert(models.Model):
    ALERT_FREQUENCY_CHOICES = [
        ("Daily", "Daily"),
        ("Weekly", "Weekly"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="job_alerts")
    # Use JSONField to store flexible search criteria
    search_query = models.JSONField(default=dict)
    frequency = models.CharField(
        max_length=10, choices=ALERT_FREQUENCY_CHOICES, default="Weekly"
    )
    last_triggered = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Job Alert for {self.user.email}"
