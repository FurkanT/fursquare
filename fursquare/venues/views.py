from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Venue, Comment, Rating, VenueType
from .serializers import VenueSerializer, CommentSerializer, VenueTypeSerializer, UserSerializer, RatingSerializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.authtoken.models import Token
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from django.contrib.auth import authenticate
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404


def main_page(request):
    venue_types = VenueType.objects.all()
    most_popular_venues = get_most_popular_venues()
    context = {
        'most_popular_venues': most_popular_venues,
        'venue_types': venue_types
    }
    return render(request, "base.html", context)


def venue_page(request, slug):
    venue_type = get_object_or_404(VenueType, slug=slug)
    venues = Venue.objects.filter(type__slug=slug)
    context = {
        'venue_type': venue_type,
        'venues': venues
    }
    return render(request, "venues.html", context)


def venue_detail_page(request, pk):
    venue = get_object_or_404(Venue, pk=pk)
    comments = paginate_comments(request, venue, 5)
    context = {
        'venue': venue,
        'comments': comments,
    }
    return render(request, "venue-detail.html", context)


def check_and_redirect_to_venue_detail(request, slug, pk):
    # venue_detail_page view is used for venue details as expected but this view is reached from the
    # e.g venue-types/restaurant/x, 'restaurant' is a slug , x is the pk.
    # the url required to reach detail of a venue from the main page is venues/x

    venue_type = get_object_or_404(VenueType, slug=slug)
    venue = get_object_or_404(Venue, pk=pk)
    venues = venue_type.venues.all()

    if venue not in venues:
        raise Http404("Venue does not exist")

    return venue_detail_page(request, pk)


@api_view(['POST'])
def login(request):

    if request.method == 'POST':
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if not user:
            return Response({"error": "Login failed"}, status=status.HTTP_401_UNAUTHORIZED)
        token, is_created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "is_created": is_created})


@api_view(['GET', 'POST'])
@permission_classes((IsAdminOrReadOnly, ))
def venue_list(request):

    if request.method == 'GET':
        venues = Venue.objects.all()
        serializer = VenueSerializer(venues, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data
        user = request.user
        data['created_by'] = user.id
        serializer = VenueSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PATCH', 'PUT', 'DELETE'])
@permission_classes((IsAdminOrReadOnly, ))
def venue_detail(request, pk):

    venue = get_object_or_404(Venue, pk=pk)

    if request.method == 'GET':
        serializer = VenueSerializer(venue)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        data = request.data
        serializer = VenueSerializer(venue, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = request.data
        serializer = VenueSerializer(venue, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    elif request.method == 'DELETE':
        venue.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes((IsAdminOrReadOnly, ))
def venue_type_list(request):

    if request.method == 'GET':
        venue_types = VenueType.objects.all()
        serializer = VenueTypeSerializer(venue_types, many=True)
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
    data = request.data

    if request.method == 'GET':
        serializer = VenueTypeSerializer(venue_type)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        serializer = VenueTypeSerializer(venue_type, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    elif request.method == 'PUT':
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
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
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
    data = request.data
    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        serializer = CommentSerializer(comment, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    elif request.method == 'PUT':
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
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PATCH', 'PUT', 'DELETE'])
@permission_classes((IsAdminOrReadOnly, ))
def user_detail(request, pk):

    user = get_object_or_404(User, pk=pk)
    data = request.data

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        serializer = UserSerializer(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticatedOrReadOnly, ))
def rating_list(request):

    if request.method == 'GET':
        ratings = Rating.objects.all()
        serializer = RatingSerializer(ratings, many=True)
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
@permission_classes((IsAuthenticatedOrReadOnly, ))
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
@permission_classes((IsOwnerOrReadOnly, ))
def venue_rating_detail(request, venue_pk, rating_pk):

    # user can reach ratings/15 but with this way , he can also reach the rating
    # if he is using api endpoint venues/2/ratings/15 (if that rating belong to venue 2)

    venue = get_object_or_404(Venue, pk=venue_pk)
    ratings = venue.ratings.all()
    rating = get_object_or_404(Rating, pk=rating_pk)
    data = request.data

    if rating not in ratings:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RatingSerializer(rating)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        serializer = RatingSerializer(rating, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = RatingSerializer(rating, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    elif request.method == 'DELETE':
        rating.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PATCH', 'PUT',  'DELETE'])
@permission_classes((IsOwnerOrReadOnly, ))
def rating_detail(request, pk):
    rating = get_object_or_404(Rating, pk=pk)
    data = request.data

    if request.method == 'GET':
        serializer = RatingSerializer(rating)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        serializer = RatingSerializer(rating, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = RatingSerializer(rating, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    elif request.method == 'DELETE':
        rating.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def get_most_popular_venues():
    venues = Venue.objects.all()
    popular_venues = sorted(venues, key=lambda obj: obj.popularity, reverse=True)[:10]
    return popular_venues


def paginate_comments(request, venue, page_number):
    comments = Comment.objects.filter(commented_to=venue)
    paginator = Paginator(comments, page_number)
    page = request.GET.get('page')
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
    return comments
