# Generated by Django 5.0 on 2024-01-05 17:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_alter_categoriedesoumission_date_limite_de_correction_avant_conference'),
    ]

    operations = [
        migrations.RenameField(
            model_name='categoriedesoumission',
            old_name='date_de_notification',
            new_name='délai_de_notification_après_soummission',
        ),
    ]
