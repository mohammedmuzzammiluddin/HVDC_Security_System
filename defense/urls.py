from django.urls import path
from . import views

app_name = 'defense'
urlpatterns = [
    path('', views.defense_dashboard, name='dashboard'),
    path('policy/toggle/<int:pk>/', views.toggle_policy, name='toggle_policy'),
    path('mitigate/<str:action_name>/', views.execute_mitigation, name='mitigate'),
]
