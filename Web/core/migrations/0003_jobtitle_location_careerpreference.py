# Generated by Django 5.1.6 on 2025-02-06 19:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_remove_profile_bio_remove_profile_birth_date_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="JobTitle",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Location",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="CareerPreference",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "min_salary",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "max_salary",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "work_type",
                    models.CharField(
                        choices=[
                            ("Remote", "Remote"),
                            ("Hybrid", "Hybrid"),
                            ("Onsite", "On-site"),
                        ],
                        default="Onsite",
                        max_length=10,
                    ),
                ),
                ("industry", models.CharField(blank=True, max_length=100)),
                (
                    "years_of_experience",
                    models.PositiveIntegerField(blank=True, null=True),
                ),
                (
                    "education_level",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("HS", "High School"),
                            ("BA", "Bachelor"),
                            ("MA", "Master"),
                            ("PhD", "PhD"),
                        ],
                        max_length=3,
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="career_preference",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "preferred_job_titles",
                    models.ManyToManyField(
                        blank=True, related_name="preferred_by", to="core.jobtitle"
                    ),
                ),
                (
                    "preferred_locations",
                    models.ManyToManyField(
                        blank=True, related_name="preferred_by", to="core.location"
                    ),
                ),
            ],
        ),
    ]
