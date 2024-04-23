import os
import boto3

import boto3.session
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

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
