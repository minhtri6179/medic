# Generated by Django 4.1.2 on 2022-12-02 04:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('prescribing_management', '0006_remove_schedule_doctor'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='doctor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='prescribing_management.doctor'),
        ),
    ]