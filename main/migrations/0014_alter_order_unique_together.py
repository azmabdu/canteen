# Generated by Django 4.1.6 on 2023-02-10 16:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_order_weekday'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='order',
            unique_together={('user', 'lunch', 'weekday')},
        ),
    ]
