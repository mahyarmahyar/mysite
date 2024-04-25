import datetime
import pandas as pd

# تبدیل مقادیر در سلول‌های اکسل به اشیاء datetime
excel_date_1 = '2024-04-15 11:21:09.260383+00:00'
excel_date_2 = '2024-04-16 11:51:01.222250+00:00'
datetime_1 = pd.to_datetime(excel_date_1)
datetime_2 = pd.to_datetime(excel_date_2)

# محاسبه‌ی اختلاف زمانی بین دو مقدار
time_difference = datetime_2 - datetime_1

# تبدیل اختلاف زمانی به ساعت
hours_difference = time_difference.total_seconds() / 3600

print("فاصله زمانی بین دو سلول به ساعت:", hours_difference)
