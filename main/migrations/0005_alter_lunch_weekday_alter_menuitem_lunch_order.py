# Generated by Django 4.1.6 on 2023-02-06 11:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_weekday_lunch_weekday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lunch',
            name='weekday',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lunch', to='main.weekday'),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='lunch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menuitem', to='main.lunch'),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lunch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lunch', to='main.lunch')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'lunch')},
            },
        ),
    ]
