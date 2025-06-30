from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Root URL - goes to dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),  # Custom logout view
    
    # Task management URLs
    path('add-task/', views.dashboard, name='add_task'),
    path('update-task-status/', views.update_task_status, name='update_task_status'),
    path('delete-task/<int:task_id>/', views.delete_task, name='delete_task'),
]