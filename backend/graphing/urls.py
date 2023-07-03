from django.urls import path
import utils


from . import views

urlpatterns = [
    path('images', views.images, name='index'),
]
