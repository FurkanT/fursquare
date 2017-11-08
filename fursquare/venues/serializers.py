from rest_framework import serializers
from .models import Venue, VenueType, Comment, Rating
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User


class VenueTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = VenueType
        fields = ('id', 'venue_type')

    def create(self, validated_data):
        return Venue.objects.create(**validated_data)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class VenueSerializer(serializers.ModelSerializer):

    venue_type = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Venue
        fields = ('id', 'venue_name', 'venue_address', 'phone_number', 'rating', 'venue_type', 'total_vote_count')

    def create(self, validated_data):
        return Venue.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.address = validated_data.get('address', instance.address)
    #     instance.phone_number = validated_data.get('phone_number', instance.phone_number)
    #     instance.language = validated_data.get('language', instance.language)
    #     instance.rating = validated_data.get('rating', instance.rating)
    #     instance.venue_type = validated_data.get('venue_type', instance.venue_type)
    #     instance.total_vote_count = validated_data.get('total_vote_count', instance.total_vote_count)
    #     instance.save()
    #     return instance

    def to_representation(self, instance):
        data = super(VenueSerializer, self).to_representation(instance)
        try:
            venue_type_id = data['venue_type']
        except KeyError:
            raise KeyError
        data['venue_type'] = get_venue_type_and_return_serialized_data(venue_type_id)
        return data


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'title', 'comment', 'commented_by', 'commented_to', 'created_date')

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.comment = validated_data.get('comment', instance.comment)
    #     instance.commented_by = validated_data.get('commented_by', instance.commented_by)
    #     instance.commented_to = validated_data.get('commented_to', instance.commented_to)
    #     instance.created_date = validated_data.get('created_date', instance.created_date)
    #     instance.save()
    #     return instance

    def to_representation(self, instance):
        data = super(CommentSerializer, self).to_representation(instance)
        try:
            user_id = data['commented_by']
        except KeyError:
            raise KeyError
        data['commented_by'] = get_user_object_and_return_serialized_data(user_id)
        try:
            venue_id = data['commented_to']
        except KeyError:
            raise KeyError
        data['commented_to'] = get_venue_object_and_return_serialized_data(venue_id)
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



# class RatingSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Rating
#
#     def create(self, validated_data):
#         return Comment.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.rating = validated_data.get('rating', instance.rating)
#         instance.total_vote_count = validated_data.get('total_vote_count', instance.total_vote_count)
#         instance.save()
#         return instance
