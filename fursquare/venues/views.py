from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from rest_framework.renderers import JSONRenderer
from .models import Venue, Comment, Rating, VenueType
from .serializers import VenueSerializer, CommentSerializer, VenueTypeSerializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly


@api_view(['GET', 'POST'])
@permission_classes((IsAdminOrReadOnly, ))
def venue_list(request):
    if request.method == 'GET':
        venue_list = Venue.objects.all()
        serializer = VenueSerializer(venue_list, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = VenueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH', 'PUT', 'DELETE'])
@permission_classes((IsAdminOrReadOnly, ))
def venue_detail(request, pk):
    try:
        venue = Venue.objects.get(pk=pk)
    except Venue.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = VenueSerializer(venue)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        data = request.data
        serializer = VenueSerializer(venue, data=data, many=True)
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
        serializer = VenueTypeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH', 'PUT', 'DELETE'])
@permission_classes((IsAdminOrReadOnly, ))
def venue_type_list_details(request, pk):
    try:
        venue_type = VenueType.objects.get(pk=pk)
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = VenueTypeSerializer(venue_type)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        data = request.data
        serializer = VenueTypeSerializer(venue_type, data=data, many=True)
        if serializer.valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        data = request.data
        serializer = VenueTypeSerializer(venue_type, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        data = request.data
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH', 'PUT',  'DELETE'])
@permission_classes((IsOwnerOrReadOnly, ))
def comment_detail(request, pk):
    try:
        comment = Comment.objects.get(pk=pk)
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        data = request.data
        serializer = VenueSerializer(comment, data=data, many=True)
        if serializer.valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        data = request.data
        serializer = CommentSerializer(comment, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes((IsAdminOrReadOnly, ))
def user_list(request):
    if request.method == 'GET':
        user_list = User.objects.all()
        serializer = VenueSerializer(user_list, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data
        serializer = VenueSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH', 'PUT', 'DELETE'])
@permission_classes((IsAdminOrReadOnly, ))
def user_detail(request, pk):
    try:
        comment = Comment.objects.get(pk=pk)
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        data = request.data
        serializer = VenueSerializer(comment, data=data, many=True)
        if serializer.valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        data = request.data
        serializer = CommentSerializer(comment, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)