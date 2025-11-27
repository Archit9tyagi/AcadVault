from django.urls import path
from . import views

urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    
    # Note-related URLs
    path('notes/', views.note_list, name='note_list'),
    path('notes/<int:pk>/', views.note_detail, name='note_detail'),
    path('notes/<int:pk>/download/', views.download_note, name='download_note'),
    path('notes/<int:pk>/delete/', views.delete_note, name='delete_note'),
    path('upload-notes/', views.upload_note, name='upload_note'),
    
    # User dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Authentication URLs
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
