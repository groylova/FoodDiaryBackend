from rest_framework import serializers

from web.models import Meal, MealComposition, FoodType, Food, PropertyFood, PFC
from web.serializers.validation import validate_pfc


class FoodSerializer(serializers.ModelSerializer):
    """Food Serializer."""
    properties = serializers.ListField(child=serializers.CharField(), required=False)
    food_type = serializers.CharField()
    protein_percent = serializers.IntegerField(required=False)
    fat_percent = serializers.IntegerField(required=False)
    carb_percent = serializers.IntegerField(required=False)
    calories_amount = serializers.IntegerField(required=False)

    class Meta:
        """Meta class."""
        model = Food
        fields = ['food_name', 'food_type', 'client', 'properties',
                  'protein_percent', 'fat_percent',
                  'carb_percent', 'calories_amount'
                  ]

    def create(self, validated_data):
        """Create function."""
        validate_pfc(validated_data)
        protein_percent = validated_data.pop('protein_percent', None)
        fat_percent = validated_data.pop('fat_percent', None)
        carb_percent = validated_data.pop('carb_percent', None)
        calories_amount = validated_data.pop('calories_amount', None)
        properties = validated_data.pop('properties', [])
        food_type = validated_data['food_type']
        validated_data['food_type'], _ = FoodType.objects.get_or_create(
            defaults={'food_type_name': food_type,
                      'client': validated_data['client']},
            food_type_name__iexact=food_type)
        food_obj, _ = Food.objects.get_or_create(
            defaults=validated_data,
            food_name__iexact=validated_data['food_name'])
        if protein_percent or fat_percent or carb_percent or calories_amount:
            PFC.objects.get_or_create(
                food=food_obj,
                protein_percent=protein_percent,
                fat_percent=fat_percent,
                carb_percent=carb_percent,
                calories_amount=calories_amount)
        for property_name in properties:
            property, _ = PropertyFood.objects.get_or_create(
                property_name__iexact=property_name)
            property.food.add(food_obj)
        return food_obj


class MealCompositionSerializer(serializers.ModelSerializer):
    """MealComposition Serializer."""
    id = serializers.ReadOnlyField()
    food = FoodSerializer(many=False)
    meal = serializers.IntegerField(source='meal.pk', required=False)
    client = serializers.IntegerField(required=False)

    class Meta:
        """Meta class."""
        model = MealComposition
        fields = ['id', 'meal', 'food', 'amount', 'percent', 'client']

    def create(self, validated_data):
        """Create method."""
        food_data = validated_data.pop('food')
        food_data['client'] = validated_data.pop('client')
        meal = validated_data.pop('meal')
        serializer = FoodSerializer(data=food_data)
        serializer.is_valid()
        food = serializer.create(validated_data=food_data)
        mc_obj = MealComposition.objects.create(
            food=food,
            meal=Meal.objects.get(id=meal),
            **validated_data
        )
        return mc_obj


class MealSerializer(serializers.ModelSerializer):
    """Meal Serializer."""
    foods = MealCompositionSerializer(many=True)
    id = serializers.ReadOnlyField()

    class Meta:
        """Meta class."""
        model = Meal
        fields = ['id', 'client', 'datetime', 'meal_type', 'foods']

    def create(self, validated_data):
        """Create function."""
        foods = validated_data.pop('foods')
        meal_obj = Meal.objects.create(**validated_data)
        for food_data in foods:
            food_data['meal'] = meal_obj.id
            food_data['client'] = meal_obj.client
            serializer = MealCompositionSerializer(data=food_data)
            serializer.is_valid()
            serializer.create(validated_data=food_data)
        return meal_obj
