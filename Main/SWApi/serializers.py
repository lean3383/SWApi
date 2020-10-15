from rest_framework import serializers
from .models import Character, World


class WorldSerial(serializers.ModelSerializer):
    class Meta:
        model = World
        fields = ('name', 'population', 'known_residents_count')

class CharacterSerial(serializers.ModelSerializer):
    homeworld = WorldSerial()

    class Meta:
        model = Character
        fields = ('name', 'height', 'mass', 'hair_color', 'skin_color',
                  'eye_color', 'birth_year', 'gender', 'homeworld',
                  'species_name', 'average_rating', 'max_rating')
