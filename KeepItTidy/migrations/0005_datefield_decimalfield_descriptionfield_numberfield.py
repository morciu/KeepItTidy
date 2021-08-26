# Generated by Django 3.1.5 on 2021-08-16 09:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('KeepItTidy', '0004_textfield_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='NumberField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('number', models.IntegerField()),
                ('collection', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='number_field', to='KeepItTidy.collection')),
            ],
        ),
        migrations.CreateModel(
            name='DescriptionField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('text', models.TextField()),
                ('collection', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='description_field', to='KeepItTidy.collection')),
            ],
        ),
        migrations.CreateModel(
            name='DecimalField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('decimal', models.DecimalField(decimal_places=2, max_digits=5)),
                ('collection', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='decimal_field', to='KeepItTidy.collection')),
            ],
        ),
        migrations.CreateModel(
            name='DateField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('date', models.DateField()),
                ('collection', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='date_field', to='KeepItTidy.collection')),
            ],
        ),
    ]