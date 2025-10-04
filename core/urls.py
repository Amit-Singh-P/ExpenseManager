from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Main pages
    path('', views.index, name='index'),
    
    # Authentication
    path('api/register/', views.register_view, name='register'),
    path('api/login/', views.login_view, name='login'),
    path('api/logout/', views.logout_view, name='logout'),
    
    # Contact
    path('api/contact/', views.contact_view, name='contact'),
    
    # Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # API endpoints
    path('api/core/', views.get_company_data, name='get_company'),
    path('api/core/update/', views.update_company, name='update_company'),
    path('api/users/', views.get_users_data, name='get_users'),
    path('api/users/create/', views.create_user, name='create_user'),
    path('api/users/<int:user_id>/update/', views.update_user, name='update_user'),
    path('api/users/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('api/stats/', views.get_dashboard_stats, name='get_stats'),
]