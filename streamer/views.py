import os
import boto3

import boto3.session
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from Levenshtein import distance as lev

from .models import User, Video, Comment, Playlist, Subscriber, Like, Dislike, Notification, UserAction

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

    if request.user.is_authenticated:
        subscribed = Subscriber.objects.filter(subscribing=user_profile, subscriber=request.user).exists()
    else:
        subscribed = False

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
        "user_profile_pic": user_profile_pic,
        "subscribed": subscribed
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

        like, dislike, in_playlist = False, False, False

        if request.user.is_authenticated:
            like = Like.objects.filter(user=request.user, video=video).exists()
            dislike = Dislike.objects.filter(user=request.user, video=video).exists()

            playlists = Playlist.objects.filter(owner=request.user)

            for playlist in playlists:
                if playlist.videos.filter(id=video_id).exists():
                    in_playlist = True
                    break
                #else:
                #    in_playlist = False
        #else:
         #   like, dislike, in_playlist = False, False, False

        comments = Comment.objects.filter(video=video)

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
            "video_file_url": video_file_url,
            "like": like,
            "dislike": dislike,
            "comments": comments,
            "in_playlist": in_playlist
        })
    
    except Video.DoesNotExist:
        return HttpResponse(status=404, reason="Video not found")


@csrf_exempt
@login_required
def action(request, action, video_id):

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    #TODO
    try:
        video = Video.objects.get(pk=video_id)

        opposite_action = "like" if action == "dislike" else "dislike"
        if UserAction.objects.filter(user=request.user, video=video, action=opposite_action).exists():
            return JsonResponse({"error": f"You have already {opposite_action}d this video"}, status=400)

        if action == "like":
            if not Like.objects.filter(user=request.user, video=video).exists():
                Like.objects.create(user=request.user, video=video)
                video.likes += 1
                video.save()
                UserAction.objects.create(user=request.user, video=video, action=action)
                return JsonResponse({"message": "Video liked successfully", "like_count": video.likes}, status=200)
            else:
                return JsonResponse({"error": "You've already liked this video"}, status=400)
        
        elif action == "dislike":
            if not Dislike.objects.filter(user=request.user, video=video).exists():
                Dislike.objects.create(user=request.user, video=video)
                video.dislikes += 1
                video.save()
                UserAction.objects.create(user=request.user, video=video, action=action)
                return JsonResponse({"message": "Video disliked successfully", "dislike_count": video.dislikes}, status=200)
            else:
                return JsonResponse({"error": "You've already disliked this video"}, status=400)
        
        else:
            return HttpResponseBadRequest("Invalid action", status=400)
        
    except Video.DoesNotExist:
        return HttpResponseNotFound("Video not found", status=404)
    

def user_videos(request, user_id, type):

    if type == "uploaded":
        uploaded_videos = Video.objects.filter(creator=user_id)
        uploaded_video_list = []

        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            config=boto3.session.Config(signature_version='s3v4'),
            region_name='eu-north-1'
        )

        for uploaded_video in uploaded_videos:
            uploaded_video_thumbnail_url = s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': str(uploaded_video.thumbnail)},
                ExpiresIn=36000
            )

            uploaded_video_data = {
                "title": uploaded_video.title,
                "creator": uploaded_video.creator.username,
                "creator_id": uploaded_video.creator.id,
                "thumbnail": uploaded_video_thumbnail_url,
                "video_id": uploaded_video.id
            }

            uploaded_video_list.append(uploaded_video_data)

        return JsonResponse({"videos": uploaded_video_list})
    
    elif type == "liked":
        liked_videos = Like.objects.filter(user=user_id)
        liked_video_list = []

        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            config=boto3.session.Config(signature_version='s3v4'),
            region_name='eu-north-1'
        )

        for liked_video in liked_videos:
            video = liked_video.video

            liked_video_thumbnail_url = s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': str(video.thumbnail)},
                ExpiresIn=36000
            )

            liked_video_data = {
                "title": video.title,
                "creator": video.creator.username,
                "creator_id": video.creator.id,
                "thumbnail": liked_video_thumbnail_url,
                "video_id": video.id
            }

            liked_video_list.append(liked_video_data)

        return JsonResponse({"videos": liked_video_list})
    
    else:
        return JsonResponse({"error": "Only type 'uploaded' and 'liked' are allowed"}, status=400)
    

@csrf_exempt
@login_required
def sub_or_unsub(request, user_id, action):

    user = User.objects.get(id=user_id)

    if action == "subscribe":
        new_subscriber = Subscriber(subscribing=user, subscriber=request.user)
        new_subscriber.save()
        return JsonResponse({"message": "Subscribed successfully!"}, status=200)
    elif action == "unsubscribe":
        try:
            remove_subscriber = Subscriber.objects.get(subscribing=user, subscriber=request.user)
            remove_subscriber.delete()
            return JsonResponse({"message": "Unsubscribed successfully!"}, status=200)
        except Subscriber.DoesNotExist:
            return JsonResponse({"error": "Subscriber relationship not found."}, status=404)
    else:
        return JsonResponse({"error": "Only subscribe and unsubscribe actions are allowed!"}, status=400)


@login_required
def comment(request, video_id):
    if request.method == "POST":
        user_comment = request.POST["comment-field"]
        video = get_object_or_404(Video, id=video_id)
        new_comment = Comment(author=request.user, video=video, text=user_comment)
        new_comment.save()
        return HttpResponseRedirect(reverse("watch_video", args=[video_id]))
    

@login_required
def subscriptions_videos(request):

    subscribed_users = Subscriber.objects.filter(subscriber=request.user).values_list('subscribing', flat=True)
    subscribed_users_videos = Video.objects.filter(creator__in=subscribed_users)
    subscribed_users_videos_list = []

    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        config=boto3.session.Config(signature_version='s3v4'),
        region_name='eu-north-1'
    )

    for subscribed_user_video in subscribed_users_videos:
        thumbnail_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': str(subscribed_user_video.thumbnail)},
            ExpiresIn=36000
        )

        subscribed_users_video_data = {
            "title": subscribed_user_video.title,
            "creator": subscribed_user_video.creator.username,
            "creator_id": subscribed_user_video.creator.id,
            "thumbnail": thumbnail_url,
            "video_id": subscribed_user_video.id
        }

        subscribed_users_videos_list.append(subscribed_users_video_data)

    return JsonResponse({"videos": subscribed_users_videos_list})


@login_required
def new_playlist(request):
    if request.method == "POST":
        playlist_name = request.POST["playlist-name"]

        try:
            new_playlist = Playlist(name=playlist_name, owner=request.user)
            new_playlist.save()
        except Exception as e:
            return HttpResponse(f"Couldn't create playlist due to an error: {str(e)}", status=500)

        return HttpResponseRedirect(reverse("index"))
    

@login_required
def get_user_playlists(request):
    try:
        playlists = Playlist.objects.filter(owner=request.user)
        playlist_names = [playlist.name for playlist in playlists]
        return JsonResponse({"playlists": playlist_names}, status=200)
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    

@csrf_exempt
@login_required
def add_to_playlist(request, playlist, video_id):
        
    try:
        
        playlist = Playlist.objects.get(name=playlist, owner=request.user)

        video = Video.objects.get(id=video_id)

        playlist.videos.add(video)

        return JsonResponse({"message": f"Video with id: {video_id} added to playlist: {playlist}"},status=200)
        
    except Exception as e:

        return JsonResponse({"error": str(e)}, status=500)
    

@login_required
def playlist_content(request, playlist):
        
    playlist = Playlist.objects.get(name=playlist, owner=request.user)
    playlist_videos = playlist.videos.all()
    playlist_videos_list = []

    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        config=boto3.session.Config(signature_version='s3v4'),
        region_name='eu-north-1'
    )

    for playlist_video in playlist_videos:
        playlist_video_thumbnail_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': str(playlist_video.thumbnail)},
            ExpiresIn=36000
        )

        playlist_video_data = {
            "title": playlist_video.title,
            "creator": playlist_video.creator.username,
            "creator_id": playlist_video.creator.id,
            "thumbnail": playlist_video_thumbnail_url,
            "video_id": playlist_video.id
        }

        playlist_videos_list.append(playlist_video_data)

    return JsonResponse({"videos": playlist_videos_list})


@login_required
@require_POST
def edit_profile(request):
        
    bio = request.POST.get('user-bio')
    pfp = request.FILES.get('user-pfp')

    user = get_object_or_404(User, id=request.user.id)
    user.bio = bio
    user.profile_pic = pfp
    user.save()

    return HttpResponseRedirect(reverse("profile", args=[request.user.id]))


def search_videos(request):
    query = request.GET.get('search')
    video_titles = Video.objects.values_list('title', flat=True)
    matched_titles = []

    for title in video_titles:
        distance = lev(query.lower(), title.lower())
        if distance <= 8:
            matched_titles.append(title)

    videos = Video.objects.filter(title__in=matched_titles)

    return render(request, "streamer/search.html", {
        "videos": videos,
        "query": query
    })