# Generated by Django 4.1.6 on 2023-02-06 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_remove_lunch_weekday_weekday_lunch'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menuitem',
            name='lunch',
        ),
        migrations.AddField(
            model_name='menuitem',
            name='lunch',
            field=models.ManyToManyField(related_name='manuitem', to='main.lunch'),
        ),
    ]
