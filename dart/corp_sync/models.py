from django.db import models

# Create your models here.
class CompanyInfo(models.Model):
    corp_code = models.CharField(max_length=8, primary_key=True)
    corp_name = models.CharField(max_length=255)
    corp_cls = models.CharField(max_length=1)
    bizr_no = models.CharField(max_length=255)
    induty_code = models.CharField(max_length=255)

    class Meta:
        db_table = 'company_info'

    def __str__(self):
        return self.corp_name

class CorpCode(models.Model):
    corp_code = models.CharField(max_length=8, primary_key=True)
    corp_name = models.CharField(max_length=255)
    stock_code = models.CharField(max_length=50)
    modify_date = models.DateField()

    class Meta:
        db_table = 'corp_code'
    def __str__(self):
        return self.corp_name
    
class History(models.Model):
    corp_code = models.CharField(max_length=20, primary_key=True)
    status = models.CharField(max_length=20)
    last_called_date = models.DateField(null=True)
    retry_count = models.IntegerField(default=0)
    created_at = models.DateField()
    updated_at = models.DateField()
    
    class Meta:
        db_table = 'history'
    

class IndustryClassification(models.Model):
    id = models.BigAutoField(primary_key=True)
    code = models.CharField(max_length=10)  # 산업 코드
    name = models.CharField(max_length=255)  # 항목명
    parent_code = models.CharField(max_length=10, null=True, blank=True)  # 상위 코드 (부모 코드)
    level = models.IntegerField()  # 계층 레벨 (예: 1 - 농업, 2 - 작물 재배업, ...)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'industry_classification'  # 테이블 이름
        
        
class CompanyIndustryView(models.Model):
    corp_code = models.CharField(max_length=10, primary_key=True)
    corp_name = models.CharField(max_length=255)
    corp_cls = models.CharField(max_length=10)
    bizr_no = models.CharField(max_length=20)
    induty_code = models.CharField(max_length=10)
    induty_name = models.CharField(max_length=255)
    level = models.CharField(max_length=20)
    category_level = models.IntegerField()

    class Meta:
        managed = False  # Django는 이 뷰에 대해 테이블을 관리하지 않음
        db_table = 'company_industry_view'  # 실제 뷰 테이블 이름