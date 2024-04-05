import main.views
from . import views
from django.urls import path



#Functions
urlpatterns = [
    path('create-assignment' , views.create_assignment , name="create-assignment"),
]



