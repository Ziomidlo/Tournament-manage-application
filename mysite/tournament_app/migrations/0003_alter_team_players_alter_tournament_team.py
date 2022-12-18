# Generated by Django 4.1.3 on 2022-12-17 20:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tournament_app', '0002_alter_team_logo_alter_tournament_logo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='players',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tournament_app.team'),
        ),
    ]