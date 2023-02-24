from rest_framework import serializers


def validate_pfc(data):
    """Validate pfc function."""
    protein_percent = data.get('protein_percent')
    fat_percent = data.get('fat_percent')
    carb_percent = data.get('carb_percent')
    if protein_percent or fat_percent or carb_percent:
        if protein_percent + fat_percent + carb_percent != 100:
            raise serializers.ValidationError("Summary of protein, fat and carbs have to equal 100%.")
