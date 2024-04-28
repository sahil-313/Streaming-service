# Generated by Django 5.0.4 on 2024-04-25 18:09

import storages.backends.s3
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streamer', '0003_alter_user_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='thumbnail',
            field=models.FileField(storage=storages.backends.s3.S3Storage(), upload_to='media/thumbnails/'),
        ),
        migrations.AlterField(
            model_name='video',
            name='video_file',
            field=models.FileField(storage=storages.backends.s3.S3Storage(), upload_to='media/videos/'),
        ),
    ]