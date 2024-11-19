from django.shortcuts import render
import requests
from pprint import pprint as pprint
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.shortcuts import get_object_or_404, get_list_or_404

from .models import Bank, Product, ProductCategory, ProductOption
from .serializers import BankListSerializer

# Create your views here.
API_KEY = settings.BANK_API_KEY

@api_view(['GET'])
def save_banks(request):
    response = requests.get(f"http://finlife.fss.or.kr/finlifeapi/companySearch.json?auth={API_KEY}&topFinGrpNo=020000&pageNo=1")
    
    # response가 정상적으로 데이터를 반환하는지 확인
    if response.status_code == 200:
        for val in response.json().get('result', {}).get('baseList', []):
            bank_name = val.get('kor_co_nm')
            bank_url = val.get('homp_url')
            bank_code = val.get('fin_co_no')
            
            if not Bank.objects.filter(bank_name=bank_name).exists():
                Bank.objects.create(bank_name=bank_name, bank_url=bank_url, bank_code=bank_code)
        
        # 성공적으로 처리된 후 응답
        data = {'title': '정상적으로 생성 되었습니다.'}
        return Response(data, status=status.HTTP_201_CREATED)
    
    # 요청이 실패했을 경우 처리
    else:
        data = {'error': '은행 정보를 가져오는 데 실패했습니다.'}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def bank_list(request):
    banks = Bank.objects.all()
    serializer = BankListSerializer(banks, many = True)

    return Response(serializer.data)

@api_view(['GET'])
def save_prdt(request):
    response = requests.get(f"http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={API_KEY}&topFinGrpNo=020000&pageNo=1")
    
    if response.status_code == 200:
        for val in response.json().get('result').get('baseList'):
            fin_code = val.get('fin_co_no')
            prdt_name = val.get('fin_prdt_nm')
            prdt_code = val.get('fin_prdt_cd')
            join_way = val.get('join_way')
            mtrt_int = val.get('mtrt_int')
            if val.get('join_deny') == '1':
              join_deny = '제한없음'
            elif val.get('join_deny') == '2':
              join_deny = '서민전용'
            elif val.get('join_deny') == '3':
              join_deny = '일부제한'
            join_member = val.get('join_member')
            etc_note = val.get('etc_note')
            max_limit = val.get('max_limit')
            bank = Bank.objects.get(bank_code = fin_code)
            product_category = ProductCategory.objects.get(pk = 1)

            if not Product.objects.filter(prdt_code = prdt_code).exists():
                Product.objects.create(
                    fin_code = fin_code,
                    prdt_name = prdt_name,
                    prdt_code = prdt_code,
                    join_way = join_way,
                    mtrt_int = mtrt_int,
                    join_deny = join_deny,
                    join_member = join_member,
                    etc_note = etc_note,
                    max_limit = max_limit,
                    bank = bank,
                    product_category = product_category
                )
        for val in response.json().get('result').get('optionList'):
            product = Product.objects.get(prdt_code = val.get('fin_prdt_cd'))
            bank = Bank.objects.get(bank_code = val.get('fin_co_no'))
            rate_type = val.get('intr_rate_type_nm')
            save_trm = val.get('save_trm')
            intr_rate = val.get('intr_rate')
            max_intr_rate = val.get('intr_rate2')

            if not ProductOption.objects.filter(product = product, save_trm = save_trm):
                ProductOption.objects.create(
                    product = product,
                    bank = bank,
                    rate_type = rate_type,
                    save_trm = save_trm,
                    intr_rate = intr_rate,
                    max_intr_rate = max_intr_rate
                )
            
        data = {'title': '정상적으로 생성 되었습니다.'}
        return Response(data, status=status.HTTP_201_CREATED)
    else:
        data = {'error': '은행 정보를 가져오는 데 실패했습니다.'}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)