from urllib import request

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.utils import timezone
from post.models import Post
from post.models import Reel

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):

    data = request.data

    title = data['title']
    content = data['content']

    image = request.FILES.get('image')
    video = request.FILES.get('video')

    post = Post.objects.create(
        user=request.user,
        title=title,
        content=content,
        image=image,
        video=video
    )

    return Response({
        'message': 'success'
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_posts(request):

    posts = Post.objects.filter(user=request.user)

    data = []

    for post in posts:

        data.append({
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'image': post.image.url if post.image else None,
            'video': post.video.url if post.video else None,
        })

    return Response(data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reel_post(request):
    data = request.data
    title=data.get('title')
    caption=data.get('caption')
    video=request.FILES.get('video')
    hashtag=data.get('hashtag')
    Reel.objects.create(user=request.user,title=title, caption=caption, video=video, hashtag=hashtag)
    print(Reel.video if Reel.video else None)
    return Response({"message":"reel post created"})

@api_view(['GET'])
@permission_classes([AllowAny])
def explore(request):
    posts=Post.objects.all()
    reels=Reel.objects.all()
    data = []
    for post in posts:
        data.append({
            'type':'post',
            'title': post.title,
            'content': post.content,
            'image': post.image.url if post.image else None,
            'video': post.video.url if post.video else None,
            'posted_by': post.user.username if post.user else None,
            'posted_on': post.updated_on.astimezone(timezone.get_current_timezone()).isoformat(),

        })

    for reel in reels:
        data.append({
            'type':'reel',
            'title': reel.title,
            'caption': reel.caption,
            'video': reel.video.url if reel.video else None,
            'hashtag': reel.hashtag,
            'posted_by': reel.user.username,
            'posted_on': reel.updated_on,

        })

    return Response(data)