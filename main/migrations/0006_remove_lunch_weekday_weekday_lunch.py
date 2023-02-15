# Generated by Django 4.1.6 on 2023-02-06 12:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_lunch_weekday_alter_menuitem_lunch_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lunch',
            name='weekday',
        ),
        migrations.AddField(
            model_name='weekday',
            name='lunch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='weekday', to='main.lunch'),
        ),
    ]