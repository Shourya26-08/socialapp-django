from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Profile, Post, Comment, Like, Follow
from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer, ProfileUpdateSerializer, PostSerializer, PostDetailSerializer, CommentSerializer, FollowUserSerializer

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or obj.author == request.user

class RegisterView(generics.CreateAPIView):
    permission_classes=[permissions.AllowAny]; serializer_class=RegisterSerializer
    def create(self,request,*a,**kw):
        s=self.get_serializer(data=request.data); s.is_valid(raise_exception=True); u=s.save(); t,_=Token.objects.get_or_create(user=u)
        return Response({'token':t.key,'username':u.username},status=201)

class LoginView(APIView):
    permission_classes=[permissions.AllowAny]
    def post(self,request):
        s=LoginSerializer(data=request.data); s.is_valid(raise_exception=True)
        u=authenticate(username=s.validated_data['username'],password=s.validated_data['password'])
        if not u: return Response({'detail':'Invalid username or password.'},status=401)
        t,_=Token.objects.get_or_create(user=u); return Response({'token':t.key,'username':u.username})

class LogoutView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def post(self,request): request.user.auth_token.delete(); return Response(status=204)

class MeView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def get(self,request): return Response(ProfileSerializer(request.user.profile,context={'request':request}).data)

class ProfileDetailView(APIView):
    permission_classes=[permissions.IsAuthenticatedOrReadOnly]
    def get(self,request,username):
        u=get_object_or_404(User,username__iexact=username); return Response(ProfileSerializer(u.profile,context={'request':request}).data)

class ProfileUpdateView(generics.UpdateAPIView):
    permission_classes=[permissions.IsAuthenticated]; serializer_class=ProfileUpdateSerializer
    def get_object(self): return self.request.user.profile
    def update(self,request,*a,**kw):
        super().update(request,*a,**kw); return Response(ProfileSerializer(self.request.user.profile,context={'request':request}).data)

class FeedView(generics.ListCreateAPIView):
    permission_classes=[permissions.IsAuthenticatedOrReadOnly]; serializer_class=PostSerializer
    def get_queryset(self):
        qs=Post.objects.select_related('author','author__profile').prefetch_related('likes','comments')
        if self.request.query_params.get('feed')=='following' and self.request.user.is_authenticated:
            ids=Follow.objects.filter(follower=self.request.user).values_list('following_id',flat=True); qs=qs.filter(author_id__in=ids)
        return qs
    def perform_create(self,s): s.save(author=self.request.user)
    def get_serializer_context(self): return {'request':self.request}

class PostDetailView(generics.RetrieveDestroyAPIView):
    queryset=Post.objects.all(); serializer_class=PostDetailSerializer; permission_classes=[permissions.IsAuthenticatedOrReadOnly,IsAuthorOrReadOnly]
    def get_serializer_context(self): return {'request':self.request}

class UserPostsView(generics.ListAPIView):
    serializer_class=PostSerializer; permission_classes=[permissions.IsAuthenticatedOrReadOnly]
    def get_queryset(self): return Post.objects.filter(author__username__iexact=self.kwargs['username'])
    def get_serializer_context(self): return {'request':self.request}

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class=CommentSerializer; permission_classes=[permissions.IsAuthenticatedOrReadOnly]
    def get_queryset(self): return Comment.objects.filter(post_id=self.kwargs['post_id'])
    def perform_create(self,s): s.save(author=self.request.user,post=get_object_or_404(Post,pk=self.kwargs['post_id']))

class CommentDeleteView(generics.DestroyAPIView):
    queryset=Comment.objects.all(); serializer_class=CommentSerializer; permission_classes=[permissions.IsAuthenticated,IsAuthorOrReadOnly]

class LikeToggleView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def post(self,request,post_id):
        p=get_object_or_404(Post,pk=post_id); _,created=Like.objects.get_or_create(post=p,user=request.user)
        return Response({'liked':True,'likes_count':p.likes.count()},status=201 if created else 200)
    def delete(self,request,post_id):
        p=get_object_or_404(Post,pk=post_id); Like.objects.filter(post=p,user=request.user).delete(); return Response({'liked':False,'likes_count':p.likes.count()})

class FollowToggleView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def post(self,request,username):
        target=get_object_or_404(User,username__iexact=username)
        if target==request.user: return Response({'detail':"You can't follow yourself."},status=400)
        _,created=Follow.objects.get_or_create(follower=request.user,following=target)
        return Response({'following':True,'followers_count':Follow.objects.filter(following=target).count()},status=201 if created else 200)
    def delete(self,request,username):
        target=get_object_or_404(User,username__iexact=username); Follow.objects.filter(follower=request.user,following=target).delete()
        return Response({'following':False,'followers_count':Follow.objects.filter(following=target).count()})

class FollowersListView(generics.ListAPIView):
    serializer_class=FollowUserSerializer; permission_classes=[permissions.IsAuthenticatedOrReadOnly]
    def get_queryset(self): return [type('Row',(),{'user':f.follower})() for f in Follow.objects.filter(following__username__iexact=self.kwargs['username']).select_related('follower__profile')]

class FollowingListView(generics.ListAPIView):
    serializer_class=FollowUserSerializer; permission_classes=[permissions.IsAuthenticatedOrReadOnly]
    def get_queryset(self): return [type('Row',(),{'user':f.following})() for f in Follow.objects.filter(follower__username__iexact=self.kwargs['username']).select_related('following__profile')]
