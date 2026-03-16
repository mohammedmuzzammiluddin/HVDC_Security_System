from django.urls import path
from . import views

app_name = 'threat_detection'
urlpatterns = [
    path('', views.threat_dashboard, name='dashboard'),
    path('run/', views.run_detection, name='run_detection'),
]
