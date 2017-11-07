from django.shortcuts import render, get_object_or_404
from . import views
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import Venue
from .serializers import VenueSerializer
from django.core.exceptions import ObjectDoesNotExist


@csrf_exempt
def venue_list(request):
    if request.method == 'GET':
        venue_list = Venue.objects.all()
        serializer = VenueSerializer(venue_list, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = VenueSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def venue_detail(request, pk):
    venue = get_object_or_404(Venue, pk=pk)

    if request.method == 'GET':
        serializer = VenueSerializer(venue)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = VenueSerializer(venue, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        venue.delete()
        return HttpResponse(status=204)
