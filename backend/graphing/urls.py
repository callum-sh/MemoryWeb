from django.urls import path
from graphing.views import PhotoView
from . import views

urlpatterns = [
    path('get-photos/', PhotoView.as_view(), name='get_photos'),
]
