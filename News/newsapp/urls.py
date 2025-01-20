
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("signup/", views.signup, name='signup'),
    path("login/", views.logins, name='login'),
    path('logout/', views.logouts, name='logout'),
    path('new-post/', views.newPost, name='newpost'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'), 
    path('uploaded-post/', views.uploadedPost, name='uploaded_post'),
    path('news/edit/<int:pk>/', views.editPost, name='news_edit'),
]

