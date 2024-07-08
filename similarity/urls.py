from django.urls import path
from .views import calculate_similarity, api_calculate_similarity

urlpatterns = [
    path('', calculate_similarity, name='calculate_similarity'),
    path('api/similarity/', api_calculate_similarity, name='api_calculate_similarity'),
]
