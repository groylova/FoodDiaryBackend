from django.db import models
from django.contrib.auth.models import User


class Custom(models.Model):
    """Custom model."""

    class Type(models.IntegerChoices):
        """Type of client."""
        client = 0
        doctor = 1

    user = models.ForeignKey(User, verbose_name='Custom')
    client_type = models.IntegerField(choices=Type.choices, verbose_name="Client or doctor")
    birth_date = models.DateField(verbose_name="Date of birth", null=True)


class Metric(models.Model):
    """Metric model."""

    class Type(models.IntegerChoices):
        """Type of metric."""
        weight = 0
        height = 1

    date = models.DateField(verbose_name="Date of event")
    metric_type = models.IntegerField(choices=Type.choices, verbose_name="Client or doctor")


class Nutrition(models.Model):
    """Nutrition model."""

    class MealType(models.IntegerChoices):
        """Type of Meal."""
        breakfast = 0
        launch = 1
        dinner = 2
        snack = 3

    client = models.ForeignKey(
        Custom,
        on_delete=models.CASCADE,
        limit_choices_to={'client_type': Custom.Type.client},
    )
    datetime = models.DateTimeField(verbose_name="Date and time of event")
    meal_type = models.IntegerField(choices=MealType.choices, verbose_name="Type of meal")


class IngredientType(models.Model):
    """IngredientType model."""
    ing_type_name = models.CharField(max_length=200, verbose_name="Ingredient type name")
    default = models.BooleanField(default=False)


class CustomIngredientType(models.Model):
    """CustomIngredientType model."""
    client = models.ForeignKey(
        Custom,
        on_delete=models.CASCADE,
        limit_choices_to={'client_type': Custom.Type.client}
    )
    ing_type = models.ForeignKey(IngredientType, on_delete=models.CASCADE)


class Ingredient(models.Model):
    """Ingredient model."""
    nutrition = models.ForeignKey(Nutrition, on_delete=models.CASCADE)
    ing_type = models.ForeignKey(IngredientType, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(verbose_name="Amount of grams")
    percent = models.PositiveIntegerField(verbose_name="Percent of portion")


class PFC(models.Model):
    """PFC model."""


class Scale(models.Model):
    """Scale model."""
    scale_name = models.CharField(max_length=200, verbose_name="Scale name")
    min_amount = models.DecimalField(null=True)
    max_amount = models.DecimalField(null=True)
    step = models.DecimalField(null=True)
    default = models.BooleanField(default=False)


class Feeling(models.Model):
    """Feeling model."""
    scale = models.ForeignKey(Scale, on_delete=models.CASCADE)
    feeling_name = models.CharField(max_length=200, verbose_name="Feeling name")
    amount = models.DecimalField(verbose_name="Amount")


class CustomScale(models.Model):
    """CustomScale model."""
    client = models.ForeignKey(
        Custom,
        on_delete=models.CASCADE,
        limit_choices_to={'client_type': Custom.Type.client}
    )
    scale = models.ForeignKey(Scale, on_delete=models.CASCADE)


class PatientTable(models.Model):
    """PatientTable model."""
    client = models.ForeignKey(
        Custom,
        on_delete=models.CASCADE,
        limit_choices_to={'client_type': Custom.Type.client},
    )
    doctor = models.ForeignKey(
        Custom,
        on_delete=models.CASCADE,
        limit_choices_to={'client_type': Custom.Type.doctor},
    )


class Goal(models.Model):
    """Goal model."""


#   Subscribe model

class Tariff(models.Model):
    """Tariff model."""


class Payment(models.Model):
    """Payment model."""


class Subscribe(models.Model):
    """Subscribe model."""

# Chat

# Rating
