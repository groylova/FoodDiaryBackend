from django.urls import path, include

from web.views import scale_view, user_view, goal_view, meal_view
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', user_view.UserViewSet)
router.register(r'groups', user_view.GroupViewSet)
router.register(r'scales', scale_view.CustomScaleViewSet)
router.register('goals', goal_view.GoalViewSet)
router.register('meals', meal_view.MealViewSet)


urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include(router.urls))
]
