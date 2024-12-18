from django.urls import path
from . import views

urlpatterns = [
    path('', views.topic_selection, name='topic_selection'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('create/', views.create_quiz, name='create_quiz'),
    path('take/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('results/<int:quiz_id>/', views.quiz_results, name='quiz_results'),
]