from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.runNordigen, name='index'),
    path('index/<str:id>/', views.goToBank, name='indexId'),
    path('profile/', views.getProfileInfo, name='profile'),
    path('profile/<str:pk>/', views.getTransactions, name='getTransactions'),
    path('profile/<str:pk>/details/', views.getDetails, name='getDetails'),
    path('profile/<str:pk>/balance/', views.getBalance, name='getBalance'),
    path('profile/<str:pk>/premium_products/', views.getPremiumProducts, name='premiumProducts'),
    path('', views.getToken, name='getToken'),
]
