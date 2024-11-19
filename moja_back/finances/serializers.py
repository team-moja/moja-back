from rest_framework import serializers
from .models import Bank, Product


class BankListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = "__all__"

class ProductListSerializer(serializers.ModelSerializer):
    bank = BankListSerializer()

    class Meta:
        model = Product
        exclude = ['fin_code', 'prdt_code', 'etc_note']

class ProductDetailSerializer(serializers.ModelSerializer):
    bank = BankListSerializer()

    class Meta:
        model = Product
        fields = '__all__'