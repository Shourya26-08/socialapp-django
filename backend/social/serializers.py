from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import Profile, Post, Comment, Like, Follow

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    bio = serializers.CharField(write_only=True, required=False, allow_blank=True, default='')
    class Meta:
        model = User
        fields = ['username','email','password','bio']
    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError('That username is already taken.')
        return value
    def create(self, data):
        bio = data.pop('bio','')
        user = User.objects.create_user(**data)
        if bio:
            user.profile.bio = bio; user.profile.save(update_fields=['bio'])
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    date_joined = serializers.DateTimeField(source='user.date_joined', read_only=True)
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    posts_count = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()
    class Meta:
        model = Profile
        fields = ['username','bio','avatar_url','date_joined','followers_count','following_count','posts_count','is_following']
    def get_followers_count(self,o): return Follow.objects.filter(following=o.user).count()
    def get_following_count(self,o): return Follow.objects.filter(follower=o.user).count()
    def get_posts_count(self,o): return o.user.posts.count()
    def get_is_following(self,o):
        request=self.context.get('request')
        if not request or not request.user.is_authenticated: return False
        if request.user == o.user: return None
        return Follow.objects.filter(follower=request.user, following=o.user).exists()

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile; fields=['bio','avatar_url']

class UserMiniSerializer(serializers.ModelSerializer):
    avatar_url=serializers.CharField(source='profile.avatar_url',read_only=True)
    class Meta:
        model=User; fields=['id','username','avatar_url']

class CommentSerializer(serializers.ModelSerializer):
    author=UserMiniSerializer(read_only=True)
    class Meta:
        model=Comment; fields=['id','post','author','content','created_at']; read_only_fields=['id','post','author','created_at']

class PostSerializer(serializers.ModelSerializer):
    author=UserMiniSerializer(read_only=True)
    likes_count=serializers.SerializerMethodField(); comments_count=serializers.SerializerMethodField(); is_liked=serializers.SerializerMethodField()
    class Meta:
        model=Post; fields=['id','author','content','image_url','created_at','likes_count','comments_count','is_liked']; read_only_fields=['id','author','created_at']
    def get_likes_count(self,o): return o.likes.count()
    def get_comments_count(self,o): return o.comments.count()
    def get_is_liked(self,o):
        r=self.context.get('request'); return bool(r and r.user.is_authenticated and o.likes.filter(user=r.user).exists())

class PostDetailSerializer(PostSerializer):
    comments=CommentSerializer(many=True,read_only=True)
    class Meta(PostSerializer.Meta): fields=PostSerializer.Meta.fields+['comments']

class FollowUserSerializer(serializers.Serializer):
    id=serializers.IntegerField(source='user.id'); username=serializers.CharField(source='user.username'); avatar_url=serializers.CharField(source='user.profile.avatar_url'); bio=serializers.CharField(source='user.profile.bio')
