# Generated by Django 3.2.7 on 2021-11-10 11:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('KeepItTidy', '0004_imagefield'),
    ]

    operations = [
        migrations.CreateModel(
            name='TempTableField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='temp_table', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
