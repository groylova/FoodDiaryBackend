from rest_framework import viewsets

from web.models import Goal
from web.serializers.goal_serializer import GoalSerializer

from django_filters.rest_framework import DjangoFilterBackend


class GoalViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Goal to be viewed or edited.

    {
        "id": 2,
        "client": 1,
        "goal_name": "balance keto kbfc",
        "description": "my goal",
        "calc_type": 1,
        "period": 1,
        "amount_of_period": 0,
        "start_date": "2023-01-01",
        "end_date": null,
        "percent": 0,
        "amount": 0,
        "pfc_goal": {
            "pfc_goal_name": "keto",
            "protein_amount": null,
            "protein_percent": 40,
            "fat_amount": null,
            "fat_percent": 40,
            "carb_amount": null,
            "carb_percent": 20,
            "calories_amount": null,
            "calories_percent": null
        },
        "scale": null
    }
    """
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['client']
