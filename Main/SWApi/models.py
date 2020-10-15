from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.cache import cache
import requests

class Ratings(models.Model):
    characterId = models.IntegerField(validators=[MinValueValidator(1)])
    rating      = models.IntegerField(validators=[MinValueValidator(1),
                                                  MaxValueValidator(5)])

class World(models.Model):
    name        = models.CharField(max_length=30)
    population  = models.CharField(max_length=30)
    known_residents_count = models.IntegerField(default=0)

class Character(models.Model):
    name           = models.CharField(max_length=30)
    height         = models.CharField(max_length=5)
    mass           = models.CharField(max_length=5)
    hair_color     = models.CharField(max_length=15)
    skin_color     = models.CharField(max_length=15)
    eye_color      = models.CharField(max_length=15)
    birth_year     = models.CharField(max_length=15)
    gender         = models.CharField(max_length=15)
    homeworld      = models.ForeignKey(World, on_delete=models.CASCADE)
    species_name   = models.CharField(max_length=15)
    average_rating = models.DecimalField(default=0, decimal_places=2,
                                                        max_digits=3)
    max_rating     = models.IntegerField(default=0)

    @classmethod
    def create(cls, id):

        if cache.get(id):
            dataPerson = cache.get(id).get('person')
            dataPlanet = cache.get(id).get('planet')
            specie     = cache.get(id).get('specie')

        else:
            url = f'https://swapi.dev/api/people/{id}/'
            dataPerson = requests.get(url).json()

            if dataPerson.get('detail') == 'Not found':
                raise ValidationError(f'{id} is not a valid value')

            url = dataPerson['homeworld']
            dataPlanet = requests.get(url).json()

            specie = 'Human'
            if dataPerson['species']:
                url = dataPerson['species'][0]
                dataSpecie = requests.get(url).json()
                specie = dataSpecie['name']

            cacheDict= {'person': dataPerson,
                        'planet': dataPlanet,
                        'specie': specie}
            cache.set(id,cacheDict)

        world = World(name=dataPlanet['name'],
                      population=dataPlanet['population'],
                      known_residents_count=len(dataPlanet['residents']))

        query    = Ratings.objects.filter(characterId=id)
        maxR     = 0
        averageR = 0
        if query:
            maxR     = max(q.rating for q in query)
            averageR = sum(q.rating for q in query)/len(query)


        return cls(name=dataPerson['name'],
                   height=dataPerson['height'],
                   mass=dataPerson['mass'],
                   hair_color=dataPerson['hair_color'],
                   skin_color=dataPerson['skin_color'],
                   eye_color=dataPerson['eye_color'],
                   birth_year=dataPerson['birth_year'],
                   gender=dataPerson['gender'],
                   homeworld=world,
                   species_name=specie,
                   average_rating=averageR,
                   max_rating=maxR
                   )
