from rest_framework import serializers

from web.models import Goal, PFC_goal
from web.serializers.validation import validate_pfc


class PFCGoalSerializer(serializers.ModelSerializer):
    """PFC_goal Serializer."""

    class Meta:
        """Meta class."""
        model = PFC_goal
        fields = ['pfc_goal_name', 'protein_amount', 'protein_percent',
                  'fat_amount', 'fat_percent', 'carb_amount', 'carb_percent',
                  'calories_amount', 'calories_percent']

    def validate(self, data):
        """Validate function."""
        validate_pfc(data)
        return super(PFCGoalSerializer, self).validate(data)


class GoalSerializer(serializers.ModelSerializer):
    """Goal Serializer."""
    pfc_goal = PFCGoalSerializer(many=False, required=False)

    class Meta:
        """Meta class."""
        model = Goal
        fields = ['id', 'client', 'goal_name', 'description', "goal_type",
                  'calc_type', 'period', 'amount_of_period', 'start_date',
                  'end_date', 'percent', 'amount', 'pfc_goal', 'scale']

    def validate(self, data):
        """Validate function."""
        goal_type = data.get('goal_type')
        amount = data.get('amount')
        scale = data.get('scale')
        if goal_type == Goal.GoalType.lose_weight and amount is None:
            raise serializers.ValidationError("You have to set amount for goal lose weight.")
        if goal_type == Goal.GoalType.find_trigger and scale is None:
            raise serializers.ValidationError("You have to set scale for goal find trigger.")
        return super(GoalSerializer, self).validate(data)

    def create(self, validated_data):
        """Create function."""
        pfc_goal = None
        if validated_data.get('pfc_goal'):
            pfc_goal_data = validated_data.pop('pfc_goal')
            serializer = PFCGoalSerializer(data=pfc_goal_data)
            serializer.is_valid()
            pfc_goal = serializer.create(pfc_goal_data)
        goal = Goal.objects.create(
            pfc_goal=pfc_goal, **validated_data)
        return goal
