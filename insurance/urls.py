from django.urls import path
from . import views

urlpatterns = [
    # Add URL for health insurance
    path('services/health-insurance/', views.health_insurance, name='health-insurance'),
    # Add URL for Life Insurance
    path('services/life-insurance/', views.life_insurance, name='life-insurance'),
    # Add URL for Auto Insurance
    path('services/auto-insurance/', views.auto_insurance, name='auto-insurance'),
    # Add URL for Home Insurance
    path('services/home-insurance/', views.home_insurance, name='home-insurance'),
    path('agent-login/', views.agent_login_view, name='agent-login'),
    path('agent-signup/', views.agent_signup_view, name='agent-signup'),
    path('agent-dashboard/', views.agent_dashboard_view, name='agent-dashboard'),
    
    path('edit-policy/<int:pk>/', views.edit_policy_view, name='edit-policy'),
    path('delete-policy/<int:pk>/', views.delete_policy_view, name='delete-policy'),
    
    
]
