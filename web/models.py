from django.db import models
from django.contrib.auth.models import User


class Custom(models.Model):
    """Custom model."""

    class Type(models.IntegerChoices):
        """Type of client."""
        client = 0
        doctor = 1

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Custom')
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
    photo_s3 = models.URLField(verbose_name="Photo of meal")
    tmp_photo = models.ImageField()  # TODO: remove in the future


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


class PropertyIngType(models.Model):
    """Property Ing Type."""
    property_name = models.CharField(max_length=200, verbose_name="Property name")
    ing_type = models.ManyToManyField(IngredientType)


class Ingredient(models.Model):
    """Ingredient model."""
    nutrition = models.ForeignKey(Nutrition, on_delete=models.CASCADE)
    ing_type = models.ForeignKey(IngredientType, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(verbose_name="Amount of grams")
    percent = models.PositiveIntegerField(verbose_name="Percent of portion")


class PFC(models.Model):
    """PFC model."""
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    protein_amount = models.PositiveIntegerField(verbose_name="Protein amount of grams")
    protein_percent = models.PositiveIntegerField(verbose_name="Protein percent of portion")
    fat_amount = models.PositiveIntegerField(verbose_name="Fat amount of grams")
    fat_percent = models.PositiveIntegerField(verbose_name="Fat percent of portion")
    carb_amount = models.PositiveIntegerField(verbose_name="Carb amount of grams")
    carb_percent = models.PositiveIntegerField(verbose_name="Carb percent of portion")
    calories_amount = models.PositiveIntegerField(verbose_name="Amount of calories")
    calories_percent = models.PositiveIntegerField(verbose_name="Calories percent of portion")


class Scale(models.Model):
    """Scale model."""
    scale_name = models.CharField(max_length=200, verbose_name="Scale name")
    scale_full_name = models.CharField(max_length=300, verbose_name="Scale full name")
    min_amount = models.DecimalField(null=True, max_digits=5, decimal_places=2, verbose_name="Min amount")
    max_amount = models.DecimalField(null=True, max_digits=5, decimal_places=2, verbose_name="Max amount")
    step = models.DecimalField(null=True, max_digits=5, decimal_places=2, verbose_name="Step")
    better_amount = models.DecimalField(null=True, max_digits=5, decimal_places=2, verbose_name="Better amount")
    default = models.BooleanField(default=False)

    def __str__(self):
        """Method str"""
        return self.scale_name


class Feeling(models.Model):
    """Feeling model."""
    scale = models.ForeignKey(Scale, on_delete=models.CASCADE)
    feeling_name = models.CharField(max_length=200, verbose_name="Feeling name")
    feeling_full_name = models.CharField(max_length=300, verbose_name="Feeling full name")
    amount = models.DecimalField(verbose_name="Amount", max_digits=5, decimal_places=2)

    def __str__(self):
        """Method str"""
        return self.feeling_name


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
        related_name="client"
    )
    doctor = models.ForeignKey(
        Custom,
        on_delete=models.CASCADE,
        limit_choices_to={'client_type': Custom.Type.doctor},
        related_name="doctor"
    )


class PFC_goal(models.Model):
    """PFC goal."""
    pfc_goal_name = models.CharField(max_length=200, verbose_name="PFC goal name.")
    protein_amount = models.PositiveIntegerField(verbose_name="Protein amount")
    protein_percent = models.PositiveIntegerField(verbose_name="Protein percent")
    fat_amount = models.PositiveIntegerField(verbose_name="Fat amount")
    fat_percent = models.PositiveIntegerField(verbose_name="Fat percent")
    carb_amount = models.PositiveIntegerField(verbose_name="Carb amount")
    carb_percent = models.PositiveIntegerField(verbose_name="Carb percent")
    calories_amount = models.PositiveIntegerField(verbose_name="Amount of calories")
    calories_percent = models.PositiveIntegerField(verbose_name="Calories percent of portion")
    default = models.BooleanField(default=False)


class CustomPFCGoal(models.Model):
    """CustomPFCGoal model."""
    client = models.ForeignKey(
        Custom,
        on_delete=models.CASCADE,
        limit_choices_to={'client_type': Custom.Type.client}
    )
    pfc_goal = models.ForeignKey(PFC_goal, on_delete=models.CASCADE)


class Goal(models.Model):
    """Goal model.

    For example: eat fewer carbs, more green vegetables, find a trigger of acne,
    don't overeat, lose weight
    """
    class CalcType(models.IntegerChoices):
        """Type of calculation."""
        whole = 0
        period = 1

    class PeriodType(models.IntegerChoices):
        """Type of period."""
        day = 0
        week = 1
        month = 2
        year = 3

    class GoalType(models.IntegerChoices):
        """Type of goal."""
        lose_weight = 0
        dont_overeat = 1
        eat_fewer_ing = 2
        eat_fewer_ing_type = 3
        eat_more_ing = 4
        eat_more_ing_type = 5
        pfc_balance = 6
        find_trigger = 7

    client = models.ForeignKey(
        Custom,
        on_delete=models.CASCADE,
        limit_choices_to={'client_type': Custom.Type.client}
    )
    goal_name = models.CharField(max_length=200, verbose_name="Goal name")
    description = models.CharField(max_length=1000, verbose_name="Description")
    calc_type = models.IntegerField(choices=CalcType.choices, verbose_name='Calculation type')
    period = models.IntegerField(choices=PeriodType.choices, verbose_name='Period type')
    amount_of_period = models.PositiveIntegerField(default=1, verbose_name='Amount of period')
    start_date = models.DateField(verbose_name='Start day')
    end_date = models.DateField(verbose_name='End date')

    percent = models.PositiveIntegerField(default=0, null=True, verbose_name='Percent for fewer or more eating')
    amount = models.PositiveIntegerField(default=0, null=True, verbose_name='Amount for fewer or more eating')
    pfc_goal = models.ForeignKey(PFC_goal, on_delete=models.CASCADE, null=True)
    feeling = models.ForeignKey(Feeling, on_delete=models.CASCADE, null=True)


#   Subscribe model

class Tariff(models.Model):
    """Tariff model."""


class Payment(models.Model):
    """Payment model."""


class Subscribe(models.Model):
    """Subscribe model."""

# Chat

# Rating of doctors
