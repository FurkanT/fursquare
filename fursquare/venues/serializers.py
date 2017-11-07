from rest_framework import serializers
from .models import Venue, VenueType
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse


class VenueTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = VenueType
        fields = ('id', 'venue_type')


class VenueSerializer(serializers.ModelSerializer):
    
    venue_type = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Venue
        fields = ('id', 'venue_name', 'venue_address', 'phone_number', 'rating', 'venue_type', 'total_vote_count')

    def create(self, validated_data):
        return Venue.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.address = validated_data.get('address', instance.address)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.language = validated_data.get('language', instance.language)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.venue_type = validated_data.get('venue_type', instance.venue_type)
        instance.total_venue_counts = validated_data.get('total_venue_counts', instance.total_venue_counts)
        instance.save()
        return instance

    def to_representation(self, instance):
        data = super(VenueSerializer, self).to_representation(instance)
        venue_type_id = data['venue_type']
        venue_type = get_object_or_404(VenueType, pk=venue_type_id)
        serializer = VenueTypeSerializer(venue_type)
        data['venue_type'] = serializer.data
        print(JsonResponse(data).content)
        return data

