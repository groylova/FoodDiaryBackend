from django.contrib import admin
from django.apps import apps
from web.models import Scale, Feeling


class ScaleAdmin(admin.ModelAdmin):
    """ScaleAdmin model"""
    list_display = [f.name for f in Scale._meta.fields]


class FeelingAdmin(admin.ModelAdmin):
    """FeelingAdmin model"""
    list_display = [f.name for f in Feeling._meta.fields]
    list_filter = ('scale',)
    search_field = ('scale',)


admin.site.register(Scale, ScaleAdmin)
admin.site.register(Feeling, FeelingAdmin)

all_models = apps.get_models()
for model in all_models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
