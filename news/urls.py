from django.urls import path
from .views import *


urlpatterns = [
    path('login', user_login, name='login'),
    path('logout', user_logout, name='logout'),
    path('register', register, name='register'),
    path('', HomeNews.as_view(), name='home'),
    path('category/<int:category_id>/', NewsByCategory.as_view(), name='category'),
    path('news/<int:pk>/', NewsView.as_view(), name='view_news'),
    path('news/add_news/', CreateNews.as_view(), name='add_news'),
]