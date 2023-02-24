from rest_framework import viewsets

from web.models import Meal
from web.serializers.meal_serializer import MealSerializer

from django_filters.rest_framework import DjangoFilterBackend


class MealViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Meal to be viewed or edited.

    {
        "client": 1,
        "meal_type": 0,
        "datetime": "2023-01-01T08:00:00",
        "foods": [
            {
                "amount": 100,
                "percent": 20,
                "food": {
                    "food_name": "buckwheat",
                    "food_type": "Cereals and potatoes",
                    "protein_percent": 40,
                    "fat_percent": 15,
                    "carb_percent": 45,
                    "calories_amount": 450,
                    "properties": ["fresh,sweet"]
                }
            },
            {
                "amount": 100,
                "percent": 80,
                "food": {
                    "food_name": "chiken file",
                    "food_type": "Fish, poultry, meat and eggs"
                }
            }
        ]
    }
    """
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['client']
