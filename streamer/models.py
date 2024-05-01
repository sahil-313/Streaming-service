from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

# Create your models here.
class User(AbstractUser):
    profile_pic = models.ImageField(storage=S3Boto3Storage(), upload_to='media/profile_pics/', blank=True, default='media/profile_pics/default-profile-pic.jpg')
    bio = models.TextField(blank=True)

class Video(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    thumbnail = models.FileField(storage=S3Boto3Storage(), upload_to='media/thumbnails/')
    category = models.CharField(max_length=50)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    video_file = models.FileField(storage=S3Boto3Storage(), upload_to='media/videos/')
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)

    def __str__(self):
        return f"Video title: {self.title} with description: {self.description} created by {self.creator}"

class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    text = models.TextField()
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
    
class Playlist(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    videos = models.ManyToManyField('Video', related_name='playlists')

    def __str__(self):
        return self.name
    
class Subscriber(models.Model):
    subscribing = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="subscribing", on_delete=models.CASCADE)
    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="subscriber", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.subscriber} is subscribed to {self.subscribing}"
    
class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} liked {self.video}"

class Dislike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    disliked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} disliked {self.video}"

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=20)
    related_video = models.ForeignKey(Video, on_delete=models.CASCADE, null=True, blank=True)
    related_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} received a {self.action_type} notification"

class UserAction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    action = models.CharField(max_length=10, choices=[('like', 'Like'), ('dislike', 'Dislike')])

    def __str__(self):
        return f"{self.user.username} {self.action}d {self.video.title}"