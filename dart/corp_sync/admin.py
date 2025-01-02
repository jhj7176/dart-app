import requests
import os 

from django.shortcuts import render
from django.contrib import admin
from corp_sync import models
from import_export.admin import ExportMixin
from import_export.formats.base_formats import XLSX

def get_company_info(api_url:str = None, corp_code:str = None, api_key:str = None):
    """
    기업개황 정보를 가져오는 함수.
    """
    params = {
        "crtfc_key": api_key,  # 인증키
        "corp_code": corp_code,  # 회사 고유 코드
    }
    response = requests.get(api_url, params=params)
    response.raise_for_status()  # HTTP 에러 발생 시 예외 처리

    # JSON 응답 데이터 파싱
    data = response.json()
    return data

@admin.register(models.CompanyInfo)
class CompanyInfoAdmin(ExportMixin, admin.ModelAdmin):
    list_display = [
        "corp_code", "corp_name", "corp_cls", "bizr_no", "induty_code"
    ]
    readonly_fields = [
        "corp_code", "corp_name", "corp_cls", "bizr_no", "induty_code"
    ]
    list_filter = ["corp_cls"]
    search_fields = ["=id", "corp_name", "corp_code"]

    # 엑셀 내보내기 기능
    def get_export_formats(self):
        formats = super().get_export_formats()
        formats.append(XLSX)  # XLSX 포맷 추가
        return formats
    
    # 액션 추가: 기업개황 API 호출
    def get_selected_corp_codes(self, request, queryset):
        corp_codes = queryset.values_list("corp_code", flat=True)
        api_results = []
        api_key = os.environ.get("API_KEY")

        for corp_code in corp_codes:
            # 기업개황 API 호출
            try:
                company_data = get_company_info(
                    api_url=f"{os.environ.get('API_HOST')}/api/company.json", 
                    api_key=api_key, 
                    corp_code=corp_code
                )
                message = company_data
                api_results.append(company_data)
                # API 호출 성공 시 메시지 추가
                self.message_user(request, message)
            except requests.exceptions.RequestException as e:
                api_results.append({'corp_code': corp_code, 'error': f"API 호출 실패: {str(e)}"})
                # 실패 메시지 추가
                self.message_user(request, f"{corp_code} API 호출 실패: {str(e)}", level='error')
        
    get_selected_corp_codes.short_description = "선택한 기업의 개황 API 호출"

    actions = [get_selected_corp_codes]
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
# CorpCode 모델 커스터마이징 등록
@admin.register(models.CorpCode)
class CorpCodeAdmin(ExportMixin, admin.ModelAdmin):
    # 리스트 화면에서 표시할 필드
    list_display = [
        "corp_code",
        "corp_name",
        "stock_code",
        "modify_date",
    ]
    
    # 읽기 전용 필드 설정
    readonly_fields = [
        "corp_code",
        "corp_name",
        "stock_code",
        "modify_date",
    ]
    
    # 액션 비활성화 (빈 리스트로 설정)
    actions = []
    
    # 필터링 옵션 추가
    list_filter = ["modify_date"]
    
    # 검색 필드 설정 (corp_code는 정확 검색, corp_name은 부분 검색 가능)
    search_fields = ["=corp_code", "corp_name"]

    # 액션을 추가하여 엑셀 내보내기 기능 활성화
    def get_export_formats(self):
        formats = super().get_export_formats()
        formats.append(XLSX)  # Add XLSX to available formats
        return formats
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
@admin.register(models.History)
class History(ExportMixin, admin.ModelAdmin):
    """
    corp_code = models.CharField(max_length=20, primary_key=True)
    status = models.CharField(max_length=20)
    last_called_date = models.DateField()
    retry_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    """
    
    list_display = [
        "corp_code",
        "status",
        "last_called_date",
        "retry_count",
        "created_at",
        "updated_at",
    ]    
    readonly_fields = [
        "corp_code",
        "status",
        "last_called_date",
        "retry_count",
        "created_at",
        "updated_at",
    ]  
         
    # 필터링 옵션 추가
    list_filter = ["status","created_at","updated_at","last_called_date"]
    
    # 검색 필드 설정 (corp_code는 정확 검색, corp_name은 부분 검색 가능)
    search_fields = ["=corp_code", "=status"]

    # 액션을 추가하여 엑셀 내보내기 기능 활성화
    def get_export_formats(self):
        formats = super().get_export_formats()
        formats.append(XLSX)  # Add XLSX to available formats
        return formats
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(models.IndustryClassification)
class IndustryClassification(ExportMixin, admin.ModelAdmin):

    list_display = [
        "id",
        "code",
        "name",
        "parent_code",
        "level",
    ]    
    readonly_fields = [
        "id",
        "code",
        "name",
        "parent_code",
        "level",
    ]  
         
    # 필터링 옵션 추가
    list_filter = ["level"]
    search_fields = ["=name", "=code"]

    # 액션을 추가하여 엑셀 내보내기 기능 활성화
    def get_export_formats(self):
        formats = super().get_export_formats()
        formats.append(XLSX)  # Add XLSX to available formats
        return formats
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(models.CompanyIndustryView)
class CompanyIndustryView(ExportMixin, admin.ModelAdmin):

    list_display = [
        "corp_code", "corp_name", "corp_cls", "bizr_no", "induty_code", "induty_name", "category_level"
    ]    
    readonly_fields = [
        "corp_code", "corp_name", "corp_cls", "bizr_no", "induty_code", "induty_name", "category_level"
    ]  
         
    # 필터링 옵션 추가
    list_filter = ["level", "corp_cls", "category_level"]
    search_fields = ["=corp_name", "=corp_code", "=induty_code"]

    # 액션을 추가하여 엑셀 내보내기 기능 활성화
    def get_export_formats(self):
        formats = super().get_export_formats()
        formats.append(XLSX)  # Add XLSX to available formats
        return formats

    # 액션 추가: 기업개황 API 호출
    def get_selected_corp_codes(self, request, queryset):
        corp_codes = queryset.values_list("corp_code", flat=True)
        api_results = []
        api_key = os.environ.get("API_KEY")

        for corp_code in corp_codes:
            # 기업개황 API 호출
            try:
                company_data = get_company_info(
                    api_url=f"{os.environ.get('API_HOST')}/api/company.json", 
                    api_key=api_key, 
                    corp_code=corp_code
                )
                message = company_data
                api_results.append(company_data)
                # API 호출 성공 시 메시지 추가
                self.message_user(request, message)
            except requests.exceptions.RequestException as e:
                api_results.append({'corp_code': corp_code, 'error': f"API 호출 실패: {str(e)}"})
                # 실패 메시지 추가
                self.message_user(request, f"{corp_code} API 호출 실패: {str(e)}", level='error')
        
    get_selected_corp_codes.short_description = "선택한 기업의 개황 API 호출"

    actions = [get_selected_corp_codes]
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False