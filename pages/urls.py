from django.urls import path
from .views import my_form_view

urlpatterns = [
    path('my-form/', my_form_view, name='my_form_view')
]