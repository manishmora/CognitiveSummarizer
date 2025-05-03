from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('viewer/<int:pk>/', views.viewer, name='viewer'),
    # path('analyze/<int:pk>/', views.analyze, name='analyze'),
]
