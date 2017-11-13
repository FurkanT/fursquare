from rest_framework import serializers
from .models import Venue, VenueType, Comment, Rating
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from drf_extra_fields.relations import PresentablePrimaryKeyRelatedField


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email')

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class VenueTypeSerializer(serializers.ModelSerializer):

    created_by = PresentablePrimaryKeyRelatedField(
        queryset=User.objects,
        presentation_serializer=UserSerializer
    )

    class Meta:
        model = VenueType
        fields = ('id', 'venue_type', 'created_by')

    def create(self, validated_data):
        return VenueType.objects.create(**validated_data)


class VenueSerializer(serializers.ModelSerializer):

    created_by = PresentablePrimaryKeyRelatedField(
        queryset=User.objects,
        presentation_serializer=UserSerializer
    )
    venue_type = PresentablePrimaryKeyRelatedField(
        queryset=VenueType.objects,
        presentation_serializer=VenueTypeSerializer
    )

    class Meta:
        model = Venue
        fields = ('id', 'venue_name', 'venue_address', 'phone_number', 'created_by', 'venue_type', 'average_rating',
                  'vote_count', )

    def create(self, validated_data):
        rating_data = validated_data.pop('rating')
        venue = Venue.objects.create(**validated_data)
        Rating.objects.create(venue=venue, **rating_data)
        return venue


class CommentSerializer(serializers.ModelSerializer):

    commented_by = PresentablePrimaryKeyRelatedField(
        queryset=User.objects,
        presentation_serializer=UserSerializer
    )
    commented_to = PresentablePrimaryKeyRelatedField(
        queryset=Venue.objects,
        presentation_serializer=VenueSerializer
    )

    class Meta:
        model = Comment
        fields = ('id', 'title', 'comment', 'commented_by', 'commented_to', 'created_date')

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)


class RatingSerializer(serializers.ModelSerializer):

    rated_by = PresentablePrimaryKeyRelatedField(
        queryset=User.objects,
        presentation_serializer=UserSerializer
    )
    venue = PresentablePrimaryKeyRelatedField(
        queryset=Venue.objects,
        presentation_serializer=VenueSerializer
    )

    class Meta:
        model = Rating
        fields = ('id', 'rating', 'venue', 'rated_by')

    def create(self, validated_data):
        return Rating.objects.create(**validated_data)


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
    return total_vote_count

