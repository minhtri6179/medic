# Generated by Django 4.1.2 on 2022-12-08 08:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prescribing_management', '0009_rename_cur_blood_pressure_prescription_cur_bood_pressure'),
    ]

    operations = [
        migrations.RenameField(
            model_name='prescription',
            old_name='cur_bood_pressure',
            new_name='cur_blood_pressure',
        ),
    ]