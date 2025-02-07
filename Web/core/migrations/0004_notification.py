# Generated by Django 5.1.6 on 2025-02-06 19:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_jobtitle_location_careerpreference'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.CharField(choices=[('Job Alert', 'Job Alert'), ('Market Trend', 'Market Trend'), ('Resource', 'Resource')], max_length=50)),
                ('content', models.TextField()),
                ('sent_date', models.DateTimeField(auto_now_add=True)),
                ('read_status', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
