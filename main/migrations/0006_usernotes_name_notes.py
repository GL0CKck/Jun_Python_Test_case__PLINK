# Generated by Django 3.2.5 on 2021-07-18 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_usernotes'),
    ]

    operations = [
        migrations.AddField(
            model_name='usernotes',
            name='name_notes',
            field=models.CharField(blank=True, max_length=122, null=True, verbose_name='Название заметки'),
        ),
    ]