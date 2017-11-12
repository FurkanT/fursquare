from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from rest_framework.renderers import JSONRenderer
from .models import Venue, Comment, Rating, VenueType
from .serializers import VenueSerializer, CommentSerializer, VenueTypeSerializer, UserSerializer, RatingSerializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.authtoken.models import Token
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from django.contrib.auth import authenticate


@api_view(["POST"])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)
    if not user:
        return Response({"error": "Login failed"}, status=status.HTTP_401_UNAUTHORIZED)
    token = Token.objects.get_or_create(user=user)
    return Response({"token": token.key})


@api_view(['GET', 'POST'])
@permission_classes((IsAdminOrReadOnly, ))
def venue_list(request):
    if request.method == 'GET':
        venue_list = Venue.objects.all()
        serializer = VenueSerializer(venue_list, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data
        user = request.user
        data['created_by'] = user.id
        serializer = VenueSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH', 'PUT', 'DELETE'])
@permission_classes((IsAdminOrReadOnly, ))
def venue_detail(request, pk):
    venue = get_object_or_404(Venue, pk=pk)

    if request.method == 'GET':
        serializer = VenueSerializer(venue)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        data = request.data
        serializer = VenueSerializer(venue, data=data, many=True, partial=True)
        if serializer.valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        data = request.data
        serializer = VenueSerializer(venue, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        venue.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes((IsAdminOrReadOnly, ))
def venue_type_list(request):
    if request.method == 'GET':
        venue_type_list = VenueType.objects.all()
        serializer = VenueTypeSerializer(venue_type_list, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data
        user = request.user
        data['created_by'] = user.id
        serializer = VenueTypeSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PATCH', 'PUT', 'DELETE'])
@permission_classes((IsAdminOrReadOnly, ))
def venue_type_detail(request, pk):
    venue_type = get_object_or_404(VenueType, pk=pk)

    if request.method == 'GET':
        serializer = VenueTypeSerializer(venue_type)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        data = request.data
        serializer = VenueTypeSerializer(venue_type, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = request.data
        serializer = VenueTypeSerializer(venue_type, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    elif request.method == 'DELETE':
        venue_type.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticatedOrReadOnly, ))
def comment_list(request):
    if request.method == 'GET':
        comment_list = Comment.objects.all()
        serializer = CommentSerializer(comment_list, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        user = request.user
        data = request.data
        data['commented_by'] = user.id
        serializer = CommentSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PATCH', 'PUT',  'DELETE'])
@permission_classes((IsOwnerOrReadOnly, ))
def comment_detail(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        data = request.data
        serializer = CommentSerializer(comment, data=data, many=True, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = request.data
        serializer = CommentSerializer(comment, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes((IsAdminOrReadOnly, ))
def user_list(request):
    if request.method == 'GET':
        user_list = User.objects.all()
        serializer = UserSerializer(user_list, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH', 'PUT', 'DELETE'])
@permission_classes((IsAdminOrReadOnly, ))
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        data = request.data
        serializer = UserSerializer(user, data=data, many=True, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = request.data
        serializer = UserSerializer(user, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes((IsAdminOrReadOnly, ))
def rating_list(request):
    if request.method == 'GET':
        rating_list = Rating.objects.all()
        serializer = RatingSerializer(rating_list, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        user = request.user
        data = request.data
        data['rated_by'] = user.id

        serializer = RatingSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
@permission_classes((IsAdminOrReadOnly, ))
def venue_rating_list(request, pk):
    venue = get_object_or_404(Venue, pk=pk)
    ratings = venue.ratings.all()

    if request.method == 'GET':
        serializer = RatingSerializer(ratings, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        user = request.user
        data = request.data
        data['rated_by'] = user.id
        data['venue'] = pk
        serializer = RatingSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PATCH', 'PUT',  'DELETE'])
@permission_classes((IsAdminOrReadOnly, ))
def venue_rating_detail(request, venue_pk, rating_pk):
    # user can reach ratings/15 but with this way , he can also reach the rating
    # if he is using api endpoint venues/2/ratings/15 (if that rating belong to venue 2)
    venue = get_object_or_404(Venue, pk=venue_pk)
    ratings = venue.ratings.objects.all()
    rating = get_object_or_404(Rating, pk=rating_pk)
    if rating not in ratings:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RatingSerializer(rating)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        data = request.data
        serializer = RatingSerializer(rating, data=data, many=True, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = request.data
        serializer = RatingSerializer(rating, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    elif request.method == 'DELETE':
        rating.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PATCH', 'PUT',  'DELETE'])
@permission_classes((IsAdminOrReadOnly, ))
def rating_detail(request, pk):
    rating = get_object_or_404(Rating, pk=pk)

    if request.method == 'GET':
        serializer = RatingSerializer(rating)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        data = request.data
        serializer = RatingSerializer(rating, data=data, many=True, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = request.data
        serializer = RatingSerializer(rating, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    elif request.method == 'DELETE':
        rating.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
