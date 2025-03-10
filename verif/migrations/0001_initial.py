# Generated by Django 5.1.7 on 2025-03-10 10:57

import django.db.models.deletion
import verif.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.PositiveIntegerField(unique=True)),
                ('user_code', models.CharField(default=verif.models.generate_user_code, max_length=10, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Enrol',
            fields=[
                ('enrol_id', models.CharField(default=verif.models.generate_enrol_id, editable=False, max_length=64, primary_key=True, serialize=False)),
                ('transaction_ref', models.CharField(max_length=255)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('depth_map', models.FileField(upload_to='depth_maps/')),
                ('confidence', models.FloatField(blank=True, null=True)),
                ('user_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='verif.user')),
            ],
        ),
    ]
