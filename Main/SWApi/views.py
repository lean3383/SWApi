from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from .models import Character, Ratings
from .serializers import CharacterSerial
import requests

@api_view(['GET'])
def getCharacter(request, id):
    try:
        elem = Character.create(id)
    except ValidationError as e:
        return Response(e, status=status.HTTP_400_BAD_REQUEST)

    elemSerial = CharacterSerial(elem)
    return Response(elemSerial.data)

@api_view(['POST'])
def setRating(request, id, rating):
    try:
        elem = Ratings(characterId=id,rating=rating)
        elem.full_clean()
        elem.save()
    except ValidationError as e:
        return Response(e, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=201)
