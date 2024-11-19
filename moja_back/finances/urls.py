from django.urls import path
from . import views

urlpatterns = [
  path('bank/', views.bank_list),
  path('bank/save/', views.save_banks),
  path('product/save-prdt/', views.save_prdt),
  path('product/save-savings/', views.save_savings),
]
