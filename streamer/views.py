import os
import boto3

import boto3.session
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth.decorators import login_required

from .models import User, Video, Comment, Playlist, Subscriber, Like, Dislike, Notification

# Create your views here.
def index(request):

    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)

        s3_client = boto3.client('s3', 
                                 aws_access_key_id=settings.AWS_ACCESS_KEY_ID, 
                                 aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                                 config=boto3.session.Config(signature_version='s3v4'),
                                 region_name='eu-north-1')
        
        user_profile_pic_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': str(user.profile_pic)},
            ExpiresIn=36000
        )

        return render(request, "streamer/index.html", {
            "user": user,
            "user_profile_pic_url": user_profile_pic_url
        })
    
    else:
        return render(request, "streamer/index.html")


@csrf_exempt
def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "streamer/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "streamer/login.html")


@csrf_exempt
def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "streamer/signup.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            if User.objects.filter(username=username).exists():
                return render(request, "streamer/signup.html", {
                    "message": "Username already taken."
                })
            
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            new_user.save()

            login(request, new_user)

            return HttpResponseRedirect(reverse("index"))
        
        except Exception as e:
            return render(request, "streamer/signup.html", {
                "message": f"An error occured: {str(e)}"
            })
    else:
        return render(request, "streamer/signup.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def profile(request, user_id):
    user_profile = User.objects.get(id=user_id)

    s3_client = boto3.client('s3', 
                                 aws_access_key_id=settings.AWS_ACCESS_KEY_ID, 
                                 aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                                 config=boto3.session.Config(signature_version='s3v4'),
                                 region_name='eu-north-1')
        
    user_profile_pic = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': str(user_profile.profile_pic)},
        ExpiresIn=36000
    )
    
    return render(request, "streamer/profile.html", {
        "user_profile": user_profile,
        "user_profile_pic": user_profile_pic
    })


@login_required
def upload_video(request):
    if request.method == 'POST':
        title = request.POST.get('video-title')
        description = request.POST.get('video-description')
        category = request.POST.get('video-category')
        thumbnail = request.FILES.get('video-thumbnail')
        video_file = request.FILES.get('video-file')

        new_video = Video(
            creator = request.user,
            title = title,
            description = description,
            category = category,
            video_file = video_file,
            thumbnail = thumbnail
        )
        new_video.save()
        
        return HttpResponseRedirect(reverse("index"))
    
    else:
        return render(request, "streamer/upload.html")


def get_videos(request):
    
    videos = Video.objects.all()
    video_list = []

    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        config=boto3.session.Config(signature_version='s3v4'),
        region_name='eu-north-1'
    )

    for video in videos:
        thumbnail_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': str(video.thumbnail)},
            ExpiresIn=36000
        )

        video_data = {
            "title": video.title,
            "creator": video.creator.username,
            "creator_id": video.creator.id,
            "thumbnail": thumbnail_url,
            "video_id": video.id
        }

        video_list.append(video_data)

    return JsonResponse({"videos": video_list})


def watch_video(request, video_id):

    try:
        video = Video.objects.get(id=video_id)

        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            config=boto3.session.Config(signature_version='s3v4'),
            region_name='eu-north-1'
        )

        video_file_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': str(video.video_file)},
            ExpiresIn=36000
        )

        return render(request, "streamer/watch.html", {
            "video": video,
            "video_file_url": video_file_url
        })
    
    except Video.DoesNotExist:
        return HttpResponse(status=404, reason="Video not found")
