from django.contrib import admin
from django.apps import apps
from web.models import Scale, Feeling, PFC_goal, Goal


class ScaleAdmin(admin.ModelAdmin):
    """ScaleAdmin model"""
    list_display = [f.name for f in Scale._meta.fields]


class FeelingAdmin(admin.ModelAdmin):
    """FeelingAdmin model"""
    list_display = [f.name for f in Feeling._meta.fields]
    list_filter = ('scale',)
    search_field = ('scale',)


class GoalAdmin(admin.ModelAdmin):
    """GoalAdmin model"""
    list_display = ['client', 'goal_name', 'goal_type']
    list_filter = ('client',)
    search_field = ('client',)


class PFC_goalAdmin(admin.ModelAdmin):
    """PFC_goal model"""
    list_display = [f.name for f in PFC_goal._meta.fields]


admin.site.register(Scale, ScaleAdmin)
admin.site.register(Feeling, FeelingAdmin)
admin.site.register(PFC_goal, PFC_goalAdmin)
admin.site.register(Goal, GoalAdmin)

all_models = apps.get_models()
for model in all_models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
