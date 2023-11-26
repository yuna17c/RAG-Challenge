from django.contrib import admin
from django.urls import path, include  # new

from pages.views import my_form_view  # Import your view function

urlpatterns = [
    path('admin/', admin.site.urls),
    path('my-form/', my_form_view, name='my_form_view'),
    # Add other URL patterns as needed
]
