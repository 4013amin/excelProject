import pandas as pd
from .models import Employee

def import_excel_data(file_path):
    df = pd.read_excel(file_path)
    for index, row in df.iterrows():
        Employee.objects.create(
            personal_code=row['کد پرسنلی'],
            first_name=row['نام'],
            last_name=row['نام خانوادگی'],
            father_name=row['نام پدر'],
            birth_date=row['تاریخ تولد'],
            insurance_date=row['تاریخ بیمه'],
            address=row['آدرس'],
            contract_duration=row['مدت قرارداد'],
            salary=row['حقوق']
        )
