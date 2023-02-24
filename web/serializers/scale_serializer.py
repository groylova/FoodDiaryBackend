from rest_framework import serializers

from web.models import CustomScale, Scale, Feeling, Custom


class CustomSerializer(serializers.ModelSerializer):
    """Custom Serializer."""

    class Meta:
        """Meta class."""
        model = Custom
        fields = ['id', 'user', 'client_type', 'birth_date']


class FeelingSerializer(serializers.ModelSerializer):
    """Feeling Serializer."""

    class Meta:
        """Meta class."""
        model = Feeling
        fields = ['feeling_name', 'feeling_full_name', 'amount']


class ScaleSerializer(serializers.ModelSerializer):
    """Scale Serializer."""

    feelings = FeelingSerializer(many=True)

    class Meta:
        """Meta."""
        model = Scale
        fields = ['scale_name', 'scale_full_name', 'min_amount', 'max_amount', 'step', 'better_amount',
                  'feelings']

    def create(self, validated_data):
        """Create function."""
        feelings_data = validated_data.pop('feelings')
        scale = Scale.objects.create(**validated_data)
        for feeling in feelings_data:
            Feeling.objects.create(scale=scale, **feeling)
        return scale


class CustomScaleSerializer(serializers.ModelSerializer):
    """CustomScale create serialazer."""

    scale = ScaleSerializer(many=False)
    client = serializers.PrimaryKeyRelatedField(queryset=Custom.objects.filter(client_type=Custom.Type.client))

    class Meta:
        """Meta."""
        model = CustomScale
        fields = ['id', 'client', 'scale']

    def create(self, validated_data):
        """Create function."""
        scale_data = validated_data.pop('scale')
        serializer = ScaleSerializer(data=scale_data)
        serializer.is_valid()
        scale = serializer.create(scale_data)
        custom_scale = CustomScale.objects.create(
            scale=scale, **validated_data)
        return custom_scale
