# Generated by Django 4.1.3 on 2022-12-19 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament_app', '0004_alter_team_description_alter_team_is_tournament_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='description',
            field=models.TextField(max_length=2000, verbose_name='Opis drużyny'),
        ),
        migrations.AlterField(
            model_name='team',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Nazwa drużyny'),
        ),
    ]