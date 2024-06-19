from django.urls import path
from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hot/', views.hot, name='hot'),
    path('question/<int:question_id>', views.question, name='question'),
    path('login/', views.login_view, name='login'),
    path('signup', views.signup, name='signup'),
    path('settings', views.settings, name='settings'),
    path('ask/', views.ask, name='ask'),
    path('tag/<str:tag_name>/', views.tag, name='tag'),
    path('logout/', views.logout, name='logout'), 
]