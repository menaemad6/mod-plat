from django.urls import path
from . import views

# Views 
urlpatterns = [
    path('wallet-recharge', views.code_charge_function, name='wallet-recharge'),
]


