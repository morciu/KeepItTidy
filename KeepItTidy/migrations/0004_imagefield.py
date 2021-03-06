# Generated by Django 3.2.7 on 2021-09-26 08:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('KeepItTidy', '0003_booleanfield'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='images/')),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image_field', to='KeepItTidy.collection')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image_field', to='KeepItTidy.item')),
            ],
        ),
    ]
