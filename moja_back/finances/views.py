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
from django.db.models import Count, Avg
from django.db.models import Q, F
from datetime import datetime

from .models import Bank, Product, ProductCategory, ProductOption, UserProducts, Exchange
from .serializers import BankListSerializer, ProductListSerializer, ProductDetailSerializer, ExchangeSerializer

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
            spcl_cnd = val.get('spcl_cnd')
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
                    spcl_cnd = spcl_cnd,
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
    
@api_view(['GET'])
def save_savings(request):
    response = requests.get(f"http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth={API_KEY}&topFinGrpNo=020000&pageNo=1")
    
    if response.status_code == 200:
        for val in response.json().get('result').get('baseList'):
            fin_code = val.get('fin_co_no')
            prdt_name = val.get('fin_prdt_nm')
            prdt_code = val.get('fin_prdt_cd')
            join_way = val.get('join_way')
            spcl_cnd = val.get('spcl_cnd')
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
            product_category = ProductCategory.objects.get(pk = 2)

            if not Product.objects.filter(prdt_code = prdt_code).exists():
                Product.objects.create(
                    fin_code = fin_code,
                    prdt_name = prdt_name,
                    prdt_code = prdt_code,
                    join_way = join_way,
                    spcl_cnd = spcl_cnd,
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
            rsrv_type = val.get('rsrv_type_nm')
            save_trm = val.get('save_trm')
            intr_rate = val.get('intr_rate')
            max_intr_rate = val.get('intr_rate2')

            if not ProductOption.objects.filter(product = product, save_trm = save_trm):
                ProductOption.objects.create(
                    product = product,
                    bank = bank,
                    rate_type = rate_type,
                    rsrv_type = rsrv_type,
                    save_trm = save_trm,
                    intr_rate = intr_rate,
                    max_intr_rate = max_intr_rate
                )
            
        data = {'title': '정상적으로 생성 되었습니다.'}
        return Response(data, status=status.HTTP_201_CREATED)
    else:
        data = {'error': '은행 정보를 가져오는 데 실패했습니다.'}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def prdt_list(request):
    product_category = ProductCategory.objects.get(pk = 1)
    products = Product.objects.filter(product_category=product_category)
    
    serializer = ProductListSerializer(products, many = True)

    return Response(serializer.data)

@api_view(['GET'])
def prdt_detail(request, pk):
    product = Product.objects.get(pk = pk)
    
    serializer = ProductDetailSerializer(product)

    return Response(serializer.data)

@api_view(['GET'])
def prdt_list(request):
    product_category = ProductCategory.objects.get(pk = 1)
    products = Product.objects.filter(product_category=product_category)
    
    serializer = ProductListSerializer(products, many = True)

    return Response(serializer.data)


@api_view(['GET'])
def prdt_detail(request, pk):
    product = Product.objects.get(pk = pk)
    
    serializer = ProductDetailSerializer(product)

    return Response(serializer.data)

@api_view(['GET'])
def savings_list(request):
    product_category = ProductCategory.objects.get(pk = 2)
    products = Product.objects.filter(product_category=product_category)
    
    serializer = ProductListSerializer(products, many = True)

    return Response(serializer.data)

@api_view(['GET'])
def savings_detail(request, pk):
    product = Product.objects.get(pk = pk)
    
    serializer = ProductDetailSerializer(product)

    return Response(serializer.data)

@api_view(['POST'])
def recommend(request):
    data = request.data
    category = data.get('category')
    user_birthday = data.get('user_birthday')  # 사용자의 생년월일
    user_age = calculate_age(user_birthday)  # 사용자의 나이를 계산

    if category == '예금':
        save_trm = data.get('save_trm')  # 예금 기간
        save_money = data.get('save_money')  # 예치 금액
        
        # 예금 추천 로직
        products = ProductOption.objects.filter(
            product__product_category__product_category='예금',
            save_trm__lte=save_trm,  # 예금 기간이 입력값보다 작거나 같음
            product__max_limit__gte=save_money  # Product의 max_limit이 예치 금액보다 크거나 같음
        ).filter(
            Q(product__max_limit__isnull=True) | Q(product__max_limit__gte=save_money)
        )

    elif category == '적금':
        save_trm = data.get('save_trm')  # 적금 기간
        save_money = data.get('save_money')  # 매월 예치할 금액
        
        # 적금 추천 로직
        products = ProductOption.objects.filter(
            product__product_category__product_category='적금',
            save_trm__lte=save_trm,  # 적금 기간이 입력값보다 작거나 같음
            product__max_limit__gte=save_money  # 적금의 경우 매월 예치금액이 max_limit보다 작거나 같아야 함
        ).filter(
            Q(product__max_limit__isnull=True) | Q(product__max_limit__gte=save_money)
        )

    # 금리 기준 추천
    max_intr_rate_product = products.order_by('-max_intr_rate').first()
    avg_intr_rate_product = products.annotate(avg_intr_rate=Avg('intr_rate')).order_by('-avg_intr_rate').first()
    max_intr_rate_actual_product = products.order_by('-intr_rate').first()

    # 1, 2, 3번 추천 항목 리스트
    recommended_products = []

    # 1. 가장 높은 max_intr_rate 상품 추천 (가장 높은 max_intr_rate)
    if max_intr_rate_product:
        recommended_products.append({
            'product_id': max_intr_rate_product.product.pk,
            'product_name': max_intr_rate_product.product.prdt_name,
            'bank_name': max_intr_rate_product.product.bank.bank_name,
            'max_intr_rate': max_intr_rate_product.max_intr_rate,
            'save_trm': max_intr_rate_product.save_trm,
            'type': 'max_intr_rate'
        })
        # 그 상품을 제외한 나머지 상품으로 추천
        remaining_products = products.exclude(id=max_intr_rate_product.id)

        # 2. 평균 금리가 높은 상품 추천
        if remaining_products.exists():
            avg_intr_rate_product = remaining_products.annotate(avg_intr_rate=Avg('intr_rate')).order_by('-avg_intr_rate').first()
            if avg_intr_rate_product:
                recommended_products.append({
                    'product_id': avg_intr_rate_product.product.pk,
                    'product_name': avg_intr_rate_product.product.prdt_name,
                    'bank_name': avg_intr_rate_product.product.bank.bank_name,
                    'avg_intr_rate': avg_intr_rate_product.avg_intr_rate,
                    'save_trm': avg_intr_rate_product.save_trm,
                    'type': 'avg_intr_rate'
                })
                # 그 상품을 제외한 나머지 상품으로 추천
                remaining_products = remaining_products.exclude(id=avg_intr_rate_product.id)

        # 3. 가장 높은 intr_rate 상품 추천
        if remaining_products.exists():
            max_intr_rate_actual_product = remaining_products.order_by('-intr_rate').first()
            if max_intr_rate_actual_product:
                recommended_products.append({
                    'product_id': max_intr_rate_actual_product.product.pk,
                    'product_name': max_intr_rate_actual_product.product.prdt_name,
                    'bank_name': max_intr_rate_actual_product.product.bank.bank_name,
                    'intr_rate': max_intr_rate_actual_product.intr_rate,
                    'save_trm': max_intr_rate_actual_product.save_trm,
                    'type': 'intr_rate'
                })

    # 연령대별 추천 상품 3개 추가
    age_group_products = get_age_group_products(user_age)

    # 전체 사용자가 가장 많이 가입한 상품 3개 추가
    top_products_by_all_users = get_top_products_by_all_users()

    # 최종 추천 상품 응답 (3개씩 그룹화하여 반환)
    return Response({
        'recommended_products': {
            'category_based_recommendations': recommended_products,
            'age_group_recommendations': age_group_products,
            'top_products_by_all_users': top_products_by_all_users,
        }
    })


def calculate_age(birth_date_str):
    """
    생년월일을 받아서 나이를 계산하는 함수
    """
    # 문자열을 datetime 객체로 변환
    birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date()
    
    today = datetime.today().date()  # 오늘 날짜
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    
    return age


def get_age_group_products(user_age):
    """
    사용자의 나이를 기반으로 연령대에서 가장 많이 가입한 상품 3개를 추천
    """
    # 연령대 구분 (예: 20대, 30대, 40대 등)
    if 20 <= user_age < 30:
        age_group = '20대'
    elif 30 <= user_age < 40:
        age_group = '30대'
    elif 40 <= user_age < 50:
        age_group = '40대'
    elif 50 <= user_age < 60:
        age_group = '50대'
    else:
        age_group = '기타'

    # 오늘 날짜를 datetime.date 형식으로 가져오기
    today = datetime.today().date()

    # 연령대별로 가입한 상품 계산
    age_group_products = UserProducts.objects.filter(
        user__birth_date__year__gte=today.year - (user_age + 10),  # 10년 후까지
        user__birth_date__year__lte=today.year - (user_age - 10)   # 10년 전부터 현재까지
    ).values('product').annotate(Count('product')).order_by('-product__count')[:3]

    recommended_age_group_products = []
    for entry in age_group_products:
        product = Product.objects.get(pk=entry['product'])
        # ProductOption에서 max_intr_rate, save_trm 값 가져오기
        product_option = ProductOption.objects.filter(product=product).first()
        recommended_age_group_products.append({
            'product_id': product.pk,
            'product_name': product.prdt_name,
            'bank_name': product.bank.bank_name,
            'max_intr_rate': product_option.max_intr_rate if product_option else None,
            'save_trm': product_option.save_trm if product_option else None,
            'type': f'age_group_{age_group}'
        })

    return recommended_age_group_products


def get_top_products_by_all_users():
    """
    전체 사용자가 가장 많이 가입한 상품 3개를 추천
    """
    top_products = UserProducts.objects.values('product').annotate(Count('product')).order_by('-product__count')[:3]
    
    recommended_top_products = []
    for entry in top_products:
        product = Product.objects.get(pk=entry['product'])
        # ProductOption에서 max_intr_rate, save_trm 값 가져오기
        product_option = ProductOption.objects.filter(product=product).first()
        recommended_top_products.append({
            'product_id': product.pk,
            'product_name': product.prdt_name,
            'bank_name': product.bank.bank_name,
            'max_intr_rate': product_option.max_intr_rate if product_option else None,
            'save_trm': product_option.save_trm if product_option else None,
            'type': 'top_product_all_users'
        })
    
    return recommended_top_products


@api_view(['GET'])
def get_exchange (request):
    EXCHANGE_API_KEY = settings.EXCHANGE_API_KEY
    response = requests.get(f'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={EXCHANGE_API_KEY}&data=AP01').json()
    exist_response = Exchange.objects.all()
    
    if response: # 가 있다면기존 데이터를 업데이트
        if not exist_response: # 쿼리셋이 비어있다면
                serializer = ExchangeSerializer(data=response, many=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data)
        else: # exist_response가 존재한다면
            Exchange.objects.all().delete()
            serializer = ExchangeSerializer(data=response, many=True)     
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
    # 없다면
    serializer = ExchangeSerializer(exist_response, many=True)
    return Response(serializer.data)
