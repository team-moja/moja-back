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

from .models import Bank
from .serializers import BankListSerializer

# Create your views here.
@api_view(['GET'])
def save_banks(request):
    API_KEY = settings.BANK_API_KEY
    response = requests.get(f"http://finlife.fss.or.kr/finlifeapi/companySearch.json?auth={API_KEY}&topFinGrpNo=020000&pageNo=1")
    
    # response가 정상적으로 데이터를 반환하는지 확인
    if response.status_code == 200:
        for val in response.json().get('result', {}).get('baseList', []):
            bank_name = val.get('kor_co_nm')
            bank_url = val.get('homp_url')
            
            if not Bank.objects.filter(bank_name=bank_name).exists():
                Bank.objects.create(bank_name=bank_name, bank_url=bank_url)
        
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