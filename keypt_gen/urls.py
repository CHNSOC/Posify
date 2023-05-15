from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('resetImage', views.resetImage, name='reset image'),
    path('imageEntrance', views.testImageResult, name='Image Entrance'),
    path('reSearchWithNewThreshold', views.reSearchWithNewThreshold, name='Search again with new threshold')
]