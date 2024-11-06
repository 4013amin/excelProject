import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
from reportlab.pdfgen import canvas

# مسیر فایل اکسل
import os

file_path = 'app/employee_data.xlsx'
if os.path.exists(file_path):
    print("File exists")
else:
    print("File does not exist")


def search_employee(request):
    personal_code = request.GET.get('personal_code')
    df = pd.read_excel(file_path)

    print(df.columns)  # نام ستون‌ها را چاپ کنید

    # بررسی و استفاده از ستون ID به جای کد پرسنلی
    try:
        # اطمینان از اینکه personal_code وجود دارد
        if personal_code is not None:
            # فیلتر کردن بر اساس ستون ID
            employee = df[df['ID'] == int(personal_code)].to_dict(orient='records')
            if employee:
                employee = employee[0]  # انتخاب اولین نتیجه به عنوان دیکشنری
            else:
                employee = None
        else:
            employee = None  # در صورت عدم وجود کد پرسنلی، employee را None قرار دهید
    except KeyError as e:
        print(f"KeyError: {e}")
        employee = None
    except ValueError as e:
        print(f"ValueError: {e}")
        employee = None

    return render(request, 'index.html', {'employee': employee})


# ویو دانلود اطلاعات کارمند به صورت PDF
def download_employee_data_pdf(request):
    personal_code = request.GET.get('personal_code')

    # بررسی وجود کد پرسنلی
    if not personal_code:
        return HttpResponse("کد پرسنلی وارد نشده است.")

    # خواندن داده‌ها از فایل اکسل
    df = pd.read_excel(file_path)
    print("Columns in DataFrame:", df.columns)  # چاپ نام ستون‌ها برای بررسی

    # بررسی اینکه آیا ستون مورد نظر وجود دارد
    if 'کد پرسنلی' not in df.columns:
        return HttpResponse("ستون 'کد پرسنلی' در فایل اکسل وجود ندارد.")

    # فیلتر کردن بر اساس کد پرسنلی
    try:
        result = df[df['کد پرسنلی'] == int(personal_code)]

        # بررسی اینکه آیا نتیجه‌ای پیدا شده یا خیر
        if result.empty:
            return HttpResponse("پرسنلی با این کد یافت نشد.")

        # دریافت داده‌های کارمند
        employee_data = result.iloc[0].to_dict()

        # ایجاد فایل PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="employee_{personal_code}.pdf"'

        pdf_canvas = canvas.Canvas(response)
        y_position = 800

        # نوشتن داده‌های کارمند در PDF
        pdf_canvas.drawString(100, y_position, "Employee Data Report")
        y_position -= 40
        for key, value in employee_data.items():
            pdf_canvas.drawString(100, y_position, f"{key}: {value}")
            y_position -= 20

        pdf_canvas.save()
        return response

    except ValueError:
        return HttpResponse("کد پرسنلی باید یک عدد صحیح باشد.")
    except Exception as e:
        return HttpResponse(f"خطا در پردازش داده‌ها: {str(e)}")
