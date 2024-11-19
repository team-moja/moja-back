from django.urls import path
from . import views

urlpatterns = [
  path('bank/', views.bank_list),
  path('bank/save/', views.save_banks),
  path('product/save/', views.save_prdt),
]
