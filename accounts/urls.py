from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('address/add/', views.add_address, name='add_address'),
    path('address/edit/<int:pk>/', views.edit_address, name='edit_address'),
    path('address/delete/<int:pk>/', views.delete_address, name='delete_address'),
]
