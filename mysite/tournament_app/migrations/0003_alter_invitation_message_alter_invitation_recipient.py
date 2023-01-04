# Generated by Django 4.1.3 on 2023-01-03 17:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tournament_app', '0002_invitation_accepted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='message',
            field=models.TextField(verbose_name='Wiadomość'),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='recipient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipient', to=settings.AUTH_USER_MODEL, to_field='username', verbose_name='Odbiorca'),
        ),
    ]