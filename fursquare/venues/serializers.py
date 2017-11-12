from rest_framework import serializers
from .models import Venue, VenueType, Comment, Rating
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


class VenueTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = VenueType
        fields = ('id', 'venue_type', 'created_by')

    def create(self, validated_data):
        return VenueType.objects.create(**validated_data)

    def to_representation(self, instance):
        data = super(VenueTypeSerializer, self).to_representation(instance)
        user_id = data['created_by']
        data['created_by'] = get_user_object_and_return_serialized_data(user_id)
        return data


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email')

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class VenueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Venue
        fields = ('id', 'venue_name', 'venue_address', 'phone_number', 'created_by', 'venue_type')

    def create(self, validated_data):
        rating_data = validated_data.pop('rating')
        venue = Venue.objects.create(**validated_data)
        Rating.objects.create(venue=venue, **rating_data)
        return venue

    def to_representation(self, instance):
        data = super(VenueSerializer, self).to_representation(instance)
        venue_type_id = data['venue_type']
        user_id = data['created_by']
        venue_id = data['id']
        data['rating'] = get_rating(venue_id)
        data['total_vote_count'] = get_vote_count(venue_id)
        data['created_by'] = get_user_object_and_return_serialized_data(user_id)
        data['venue_type'] = get_venue_type_and_return_serialized_data(venue_type_id)
        return data


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'title', 'comment', 'commented_by', 'commented_to', 'created_date')

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)

    def to_representation(self, instance):
        data = super(CommentSerializer, self).to_representation(instance)
        user_id = data['commented_by']
        data['commented_by'] = get_user_object_and_return_serialized_data(user_id)
        venue_id = data['commented_to']
        data['commented_to'] = get_venue_object_and_return_serialized_data(venue_id)
        return data


class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = ('id', 'rating', 'venue', 'rated_by')

    def create(self, validated_data):
        return Rating.objects.create(**validated_data)

    def to_representation(self, instance):
        data = super(RatingSerializer, self).to_representation(instance)
        venue_id = data['venue']
        data['venue'] = get_venue_object_and_return_serialized_data(venue_id)
        user_id = data['rated_by']
        data['rated_by'] = get_user_object_and_return_serialized_data(user_id)
        data['rating'] = str(data['rating'])
        return data


def get_venue_object_and_return_serialized_data(venue_id):
    venue = get_object_or_404(Venue, pk=venue_id)
    serializer = VenueSerializer(venue)
    return serializer.data


def get_user_object_and_return_serialized_data(user_id):
    user = get_object_or_404(User, pk=user_id)
    serializer = UserSerializer(user)
    return serializer.data


def get_venue_type_and_return_serialized_data(venue_type_id):
    venue_type = get_object_or_404(VenueType, pk=venue_type_id)
    serializer = VenueTypeSerializer(venue_type)
    return serializer.data


def get_rating(venue_id):
    venue = get_object_or_404(Venue, pk=venue_id)
    rate = venue.average_rating
    return rate


def get_vote_count(venue_id):
    venue = get_object_or_404(Venue, pk=venue_id)
    total_vote_count = venue.vote_count
    return str(total_vote_count)

