from rest_framework import viewsets

from web.models import CustomScale
from web.serializers.scale_serializer import CustomScaleSerializer

from django_filters.rest_framework import DjangoFilterBackend


class CustomScaleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows CustomScale to be viewed or edited.

    {
        "client": 1,
        "scale": {
            "scale_name": "migrene-1",
            "scale_full_name": "scale of pain",
            "min_amount": 0,
            "max_amount": 4,
            "step": 1,
            "better_amount": 0,
            "feelings": [
                { "feeling_name": "no_pain", "feeling_full_name": "no pain", "amount": 0 },
                { "feeling_name": "mild_pain", "feeling_full_name": "mild pain", "amount": 1 },
                { "feeling_name": "unpleasant_pain", "feeling_full_name": "unpleasant pain", "amount": 2 },
                { "feeling_name": "strong_pain", "feeling_full_name": "strong pain", "amount": 3 },
                { "feeling_name": "unbearable_pain", "feeling_full_name": "unbearable pain", "amount": 4 }
            ]
        }
    }
    """
    queryset = CustomScale.objects.all()
    serializer_class = CustomScaleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['client']
