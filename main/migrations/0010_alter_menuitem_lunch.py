# Generated by Django 4.1.6 on 2023-02-06 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_weekday_lunch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='lunch',
            field=models.ManyToManyField(related_name='menuitem', to='main.lunch'),
        ),
    ]
