import time
import requests
from celery import shared_task
from datetime import datetime
from .models import CompanyInfo, History, CorpCode
from django.db import transaction, models
import os

# API 설정
API_URL = f"{os.environ.get('API_HOST')}/api/company.json"
API_KEY = os.environ.get("API_KEY")

# 최대 재시도 횟수
MAX_RETRIES = 10


# 1차 태스크: 큐에 작업 등록
@shared_task
def enqueue_pending_codes():
    """
    'pending' 상태의 코드 18,000개를 큐에 등록.
    """
    print("enqueue_pending_codes start")
    # pending_codes = History.objects.filter(status='pending').values_list('corp_code', flat=True)[:38000]
    pending_codes = History.objects.filter(status='pending').values_list('corp_code', flat=True)
    print(f"enqueue_pending_codes task is being executed {len(pending_codes)}")
    for corp_code in pending_codes:
        # 개별 코드 처리 태스크 등록
        process_single_code.delay(corp_code)
    print("enqueue_pending_codes end")

# 1차 태스크: 큐에 작업 등록
@shared_task
def enqueue_unusal_codes():
    """
    'pending' 상태의 코드 18,000개를 큐에 등록.
    """
    pending_codes = History.objects.filter(status='pending').values_list('corp_code', flat=True)[:36000]

    for corp_code in pending_codes:
        # 개별 코드 처리 태스크 등록
        process_single_code.delay(corp_code)

# 2차 태스크: 개별 코드 처리
@shared_task
def process_single_code(corp_code):
    """
    단일 corp_code 처리 및 재시도 관리
    """
    retry_count = 0  # 재시도 횟수 초기화
    success = False  # 성공 여부 플래그

    while retry_count < MAX_RETRIES:
        # API 요청
        status, company_data = get_company_info(API_URL, corp_code, API_KEY)

        if status == "OK":  # 성공
            success = True
            with transaction.atomic():
                # CompanyInfo 업데이트
                # CompanyInfo.objects.create(**company_data)
                company_info, created = CompanyInfo.objects.update_or_create(
                    corp_code=corp_code,
                    defaults=company_data
                )
                
                # History 업데이트
                History.objects.update_or_create(
                    corp_code=corp_code,
                    defaults={
                        'status': 'success',
                        'last_called_date': datetime.now(),
                        'retry_count': retry_count
                    }
                )
            break  # 성공 시 종료

        else:  # 실패 시 재시도
            print(f"retry_count: {retry_count} / corp_code:{corp_code}")
            retry_count += 1
            time.sleep(1)  # 1초 대기

    # 5회 실패 시 상태 'failed' 처리
    if not success:
        History.objects.filter(corp_code=corp_code).update(
            status='failed', retry_count=models.F('retry_count') + retry_count
        )


# API 호출 함수
def get_company_info(api_url, corp_code, api_key):
    """
    API 호출을 통해 회사 정보를 가져옵니다.
    """
    try:
        params = {
            "crtfc_key": api_key,
            "corp_code": corp_code,
        }
        response = requests.get(api_url, params=params)
        response.raise_for_status()

        data = response.json()
        if data['status'] != "000":  # API 상태 코드가 정상(000)이 아닐 경우
            return "FAIL", data

        # 성공 시 데이터 반환
        result = {
            "corp_name": data.get("corp_name"),
            "corp_cls": data.get("corp_cls"),
            "bizr_no": data.get("bizr_no"),
            "induty_code": data.get("induty_code"),
            "corp_code" : corp_code,
        }
        return "OK", result
    except Exception as e:
        print(f"Request error: {e}")
        return "ERROR", {f"{type(e).__name__}":f"{e}"}