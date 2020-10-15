from django.urls import path
from . import views

urlpatterns = [
    path('character/<int:id>/', views.getCharacter ),
    path('character/<int:id>/<int:rating>/', views.setRating ),
]
