from django.urls import path
from . import views
from .views import generate_email_reply

urlpatterns = [
    
     path('', views.landing, name='landing'),

    # Login
    path('login/', views.login_view, name='login'),

    # Register
    path('register/', views.register_view, name='register'),

    # Logout
    path('logout/', views.logout_view, name='logout'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('update-profile/', views.update_profile, name='update_profile'),

    # CRUD
    path('create/', views.create_reply, name='create'),

    path('history/', views.history, name='history'),

    path('update/<int:id>/', views.update_reply, name='update'),

    path('delete/<int:id>/', views.delete_reply, name='delete'),
    
    path('generate-reply/', generate_email_reply, name='generate_reply'),
]





