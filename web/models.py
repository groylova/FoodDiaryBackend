from django.db import models
from django.contrib.auth.models import User


# Clients
class Custom(models.Model):
    """Custom model."""

    class Type(models.IntegerChoices):
        """Type of client."""
        client = 0
        doctor = 1

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Custom')
    client_type = models.IntegerField(choices=Type.choices, verbose_name="Client or doctor")
    birth_date = models.DateField(verbose_name="Date of birth", null=True)

    def __str__(self):
        """Method str"""
        return self.user.username


class Metric(models.Model):
    """Metric model."""

    class Type(models.IntegerChoices):
        """Type of metric."""
        weight = 0
        height = 1

    date = models.DateField(verbose_name="Date of event")
    metric_type = models.IntegerField(choices=Type.choices, verbose_name="Client or doctor")


# Meal
class Meal(models.Model):
    """Meal model."""

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


class FoodType(models.Model):
    """FoodType model."""
    food_type_name = models.CharField(max_length=200, verbose_name="Food type name")
    default = models.BooleanField(default=False)
    client = models.ForeignKey(
        Custom,
        on_delete=models.CASCADE,
        limit_choices_to={'client_type': Custom.Type.client},
        null=True
    )

    def __str__(self):
        """Method str"""
        return self.food_type_name


class Food(models.Model):
    """Food model."""
    food_name = models.CharField(max_length=200, verbose_name="Food name")
    food_type = models.ForeignKey(FoodType, on_delete=models.CASCADE)
    client = models.ForeignKey(
        Custom,
        on_delete=models.CASCADE,
        limit_choices_to={'client_type': Custom.Type.client},
        null=True
    )

    def __str__(self):
        """Method str"""
        return self.food_name


class PropertyFood(models.Model):
    """Property Food."""
    property_name = models.CharField(max_length=200, verbose_name="Property name")
    default = models.BooleanField(default=False)
    food = models.ManyToManyField(Food)


class MealComposition(models.Model):
    """MealComposition model."""
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name="foods")
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name="meals")
    amount = models.PositiveIntegerField(verbose_name="Amount of grams")
    percent = models.PositiveIntegerField(verbose_name="Percent of portion")


class PFC(models.Model):
    """PFC model."""
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    protein_percent = models.PositiveIntegerField(verbose_name="Protein percent of portion")
    fat_percent = models.PositiveIntegerField(verbose_name="Fat percent of portion")
    carb_percent = models.PositiveIntegerField(verbose_name="Carb percent of portion")
    calories_amount = models.PositiveIntegerField(verbose_name="Amount of calories")


# Goal
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
    scale = models.ForeignKey(Scale, on_delete=models.CASCADE, related_name='feelings')
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
    protein_amount = models.PositiveIntegerField(verbose_name="Protein amount", null=True)
    protein_percent = models.PositiveIntegerField(verbose_name="Protein percent", null=True)
    fat_amount = models.PositiveIntegerField(verbose_name="Fat amount", null=True)
    fat_percent = models.PositiveIntegerField(verbose_name="Fat percent", null=True)
    carb_amount = models.PositiveIntegerField(verbose_name="Carb amount", null=True)
    carb_percent = models.PositiveIntegerField(verbose_name="Carb percent", null=True)
    calories_amount = models.PositiveIntegerField(verbose_name="Amount of calories", null=True)
    calories_percent = models.PositiveIntegerField(verbose_name="Calories percent of portion", null=True)
    default = models.BooleanField(default=False)

    def __str__(self):
        """Method str"""
        return self.pfc_goal_name


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
        custom = 4

    class GoalType(models.IntegerChoices):
        """Type of goal."""
        lose_weight = 0
        gain_weight = 1
        dont_overeat = 2
        eat_fewer_ing = 3
        eat_fewer_ing_type = 4
        eat_more_ing = 5
        eat_more_ing_type = 6
        pfc_balance = 7
        find_trigger = 8

    client = models.ForeignKey(
        Custom,
        on_delete=models.CASCADE,
        limit_choices_to={'client_type': Custom.Type.client}
    )
    goal_name = models.CharField(max_length=200, verbose_name="Goal name")
    goal_type = models.IntegerField(choices=GoalType.choices, verbose_name='Goal type')
    description = models.CharField(max_length=1000, verbose_name="Description")
    calc_type = models.IntegerField(choices=CalcType.choices, verbose_name='Calculation type')
    period = models.IntegerField(choices=PeriodType.choices, verbose_name='Period type')
    amount_of_period = models.PositiveIntegerField(default=0, verbose_name='Amount of period for trigger')
    start_date = models.DateField(verbose_name='Start day')
    end_date = models.DateField(verbose_name='End date', null=True)

    percent = models.PositiveIntegerField(default=0, null=True, verbose_name='Percent for fewer or more eating')
    amount = models.PositiveIntegerField(default=0, null=True, verbose_name='Amount for fewer or more eating')
    pfc_goal = models.ForeignKey(PFC_goal, on_delete=models.CASCADE, null=True)
    scale = models.ForeignKey(Scale, on_delete=models.CASCADE, null=True)

    def __str__(self):
        """Method str"""
        return self.goal_name

#   Subscribe model

class Tariff(models.Model):
    """Tariff model."""


class Payment(models.Model):
    """Payment model."""


class Subscribe(models.Model):
    """Subscribe model."""

# Chat

# Rating of doctors
