from django.urls import path
from . import views

app_name = 'simulation'
urlpatterns = [
    path('', views.scenario_list, name='scenarios'),
    path('run/<int:pk>/', views.run_scenario, name='run'),
    path('results/', views.results, name='results'),
]
