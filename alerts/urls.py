from django.urls import path
from . import views

app_name = 'alerts'
urlpatterns = [
    path('', views.alert_list, name='list'),
    path('resolve/<int:pk>/', views.resolve_alert, name='resolve'),
    path('preferences/', views.preferences, name='preferences'),
]
