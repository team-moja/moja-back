from django.urls import path
from . import views

urlpatterns = [
  path('bank/save/', views.save_banks),
  # path('bank/save/', views.save_banks),
]
