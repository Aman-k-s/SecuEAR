from django.urls import path
from .views import upload_file, home, landing

urlpatterns = [
    path('', home, name='home'),
    path('upload/', upload_file, name='upload_file'),
    path('landing/<str:enrol_id>', landing, name='landing'),
]
