import calendar
import math
import random
from datetime import datetime, timedelta
from app.backend.classes.hr_final_day_month_class import HrFinalDayMonthClass
import calendar
from dateutil.relativedelta import relativedelta

class HelperClass:

    def add_business_days(start_date, num_days, holidays):
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        current_date = start_date
        added_days = 0
        while added_days < int(num_days):
            # sumamos un día a la fecha actual
            current_date += timedelta(days=1)
            # verificamos si la fecha actual es hábil/laboral
            if calendar.weekday(current_date.year, current_date.month, current_date.day) < 5:
                added_days += 1

        # sumamos los días feriados al resultado si la lista no está vacía
        if holidays > 0:
            current_date += timedelta(days=holidays)

        return current_date
    
    def count_weekends(start_date, end_date):
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        if end_date.weekday() == 5:  # Si es viernes (0=Lunes, 6=Domingo)
            end_date += timedelta(days=2)  # Suma 2 dias
        weekend_count = 0
        delta = timedelta(days=1)
        current_date = start_date
        while current_date <= end_date:
            if current_date.weekday() >= 5:  # Si es sábado o domingo
                weekend_count += 1
            current_date += delta

        return weekend_count
    
    def vacation_day_value(amount):
        value = math.ceil(amount/30)

        return value

    def gratification(salary): 
        return math.ceil(salary*0.25)
    
    def get_end_document_total_years(self, start_year, end_year):
        date1 = datetime.strptime(str(start_year), "%Y-%m-%d")
        date2 = datetime.strptime(str(end_year), "%Y-%m-%d")

        delta = date2 - date1

        years = delta.days/365
        months = self.split(end_year,'-')

        if years >= 1:
            if int(months[1]) >=6:
                years = years + 1
        else:
            years = 0

        return math.ceil(years)

    def months_to_years(self, months):
        years = int(months/12)

        return years

    def vacation_days(self, months, extreme_zone_status_id):
        if months > 0:
            if extreme_zone_status_id == 1:
                total = math.ceil(float((months+1))*float(1.66))
            else:
                total = math.ceil((float(months+1)) * float(1.25))
        else:
            total = 0
            
        return total
    
    def progressive_vacation_days(self, months, extreme_zone_status_id):
        if months > 0:
            if extreme_zone_status_id == 1:
                total = math.ceil(float((months+1))*float(1.66))
            else:
                total = math.ceil((float(months+1)) * float(1.25))
        else:
            total = 0
            
        return total
    
    def numeric_rut(self, rut):
        rut = rut.split('-')

        return rut[0]
    
    def upper_string(self, string):
        result = string.upper()

        return result
    
    def split(self, value, separator):
        value = value.split(separator)

        return value
    
    def months(self, since, until):
        since_array = self.split(str(since), "-")
        until_array = self.split(str(until), "-")

        if since != None and until != None:
            if until_array[0] != '' and since_array[0] != '':
                return (int(until_array[0]) - int(since_array[0])) * 12 + int(until_array[1]) - int(since_array[1])
            else:
                return 0
        else:
            return 0
        
    def remove_from_string(self, value_to_remove, string):
        string = string.replace(value_to_remove, "")

        return string
    
    def add_zero(self, number):
        if number < 10:
            result = "0" + str(number)
        else:
            result = number

        return result
    
    def file_name(self, rut, description):
        now = datetime.now()

        current_year = now.year
        current_month = now.month
        current_day = now.day

        current_month = self.add_zero(current_month)

        random_float = random.randint(1, 9999999999999999)

        file_name = str(random_float) + "_" + str(rut) + "_" + str(description) + "_" + str(current_day) + "_" + str(current_month) + "_" + str(current_year)

        return file_name
    
    def nickname(self, name, lastname):
        nickname = str(name) + ' ' + str(lastname) 

        return nickname
    
    def days(self, since, until, no_valid_entered_days = 0):
        # Definir las fechas de inicio y finalización
        start_date = datetime.strptime(since, "%Y-%m-%d")
        end_date = datetime.strptime(until, "%Y-%m-%d")

        # Calcular la cantidad de días hábiles entre las dos fechas
        num_business_days = 0
        current_date = start_date
        while current_date <= end_date:
            if current_date.weekday() < 5:
                num_business_days += 1
            current_date += timedelta(days=1)

        return int(num_business_days)
    
    def numeric_rut(self, rut):
        rut = rut.split('-')

        return rut[0]
    
    def final_day_month(self, month):
        if month == '1':
            return { "end_day": 31, "adjustment_day": -1 },
        elif month == '2':
            return { "end_day": 28, "adjustment_day": 2 }
        elif month == '3':
            return { "end_day": 30, "adjustment_day": 0 }
        elif month == '4':
            return { "end_day": 31, "adjustment_day": -1 }
        elif month == '5':
            return { "end_day": 30, "adjustment_day": 0 }
        elif month == '6':
            return { "end_day": 30, "adjustment_day": 0 }
        elif month == '7':
            return { "end_day": 31, "adjustment_day": -1 }
        elif month == '8':
            return { "end_day": 31, "adjustment_day": -1 }
        elif month == '9':
            return { "end_day": 30, "adjustment_day": 0 }
        elif month == '10':
            return { "end_day": 31, "adjustment_day": -1 }
        elif month == '11':
            return { "end_day": 30, "adjustment_day": 0 }
        elif month == '12':
            return { "end_day": 31, "adjustment_day": -1 }
    
    def get_time_Y_m_d(self):
        return datetime.now().strftime('%Y-%m-%d')

    def count_months(since_date, until_date):
        since_date = datetime.strptime(since_date, '%Y-%m-%d')
        until_date = datetime.strptime(until_date, '%Y-%m-%d')
        
        months = 0
        
        while since_date <= until_date:
            months += 1
            
            if since_date.month == 12:
                since_date = since_date.replace(year=since_date.year + 1, month=1, day=1)
            else:
                since_date = since_date.replace(month=since_date.month + 1, day=1)
        
        return months
    
    def get_periods(self, since, until):
        format = "%Y-%m-%d"
        start_obj = datetime.strptime(since, format)
        end_obj = datetime.strptime(until, format)

        # Calcula la diferencia entre las dos fechas
        diference = end_obj - start_obj

        # Obtiene la cantidad de días
        days = diference.days

        # Si las fechas están en el mismo mes, no suma 1, de lo contrario, suma 1
        if start_obj.month != end_obj.month:
            days += 1

        splited_since = since.split("-")
        splited_until = until.split("-")
        how_many_months = HelperClass.count_months(since, until)

        if how_many_months == 1:
            first_since = since
            first_until = until
            d1 = datetime.strptime(first_since, "%Y-%m-%d")
            d2 = datetime.strptime(first_until, "%Y-%m-%d")
            first_days = abs((d2 - d1).days)
            first_days = first_days + 1

            data = [[first_since, first_until, first_days]]
        elif how_many_months == 2:
            final_day = self.final_day_month(str(splited_since[1]))
            final_day = final_day['end_day']
            first_since = since
            first_until = splited_since[0] +'-'+ splited_since[1] + '-' + str(final_day)
            d1 = datetime.strptime(first_since, "%Y-%m-%d")
            d2 = datetime.strptime(first_until, "%Y-%m-%d")
            first_days = abs((d2 - d1).days)
            first_days = first_days + 1

            second_since = splited_until[0] +'-'+ splited_until[1] + '-01'
            second_until = until
            d1 = datetime.strptime(second_since, "%Y-%m-%d")
            d2 = datetime.strptime(second_until, "%Y-%m-%d")
            second_days = abs((d2 - d1).days)
            second_days = second_days + 1

            data = [[first_since, first_until, first_days], [second_since, second_until, second_days]]
        else:
            final_day = self.final_day_month(str(splited_since[1]))
            final_day = final_day['end_day']
            first_since = since
            first_until = splited_since[0] +'-'+ splited_since[1] + '-' + str(final_day)
            d1 = datetime.strptime(first_since, "%Y-%m-%d")
            d2 = datetime.strptime(first_until, "%Y-%m-%d")
            first_days = abs((d2 - d1).days)
            first_days = first_days + 1
            
            middle_month = int(splited_since[1]) + 1
            final_day = self.final_day_month(str(middle_month))
            final_day = final_day['end_day']
            second_since = str(splited_until[0]) +'-'+ str(middle_month) + '-01'
            second_until = str(splited_until[0]) +'-'+ str(middle_month) + '-' + str(final_day)
            d1 = datetime.strptime(second_since, "%Y-%m-%d")
            d2 = datetime.strptime(second_until, "%Y-%m-%d")
            second_days = abs((d2 - d1).days)
            second_days = second_days + 1

            splited_since = second_since.split("-")
            splited_until = second_until.split("-")

            middle_month = int(splited_since[1]) + 1
            third_since = splited_until[0] +'-'+ str(middle_month) + '-01'
            third_until = until
            d1 = datetime.strptime(third_since, "%Y-%m-%d")
            d2 = datetime.strptime(third_until, "%Y-%m-%d")
            third_days = abs((d2 - d1).days)
            third_days = third_days + 1

        return data

    def progressive_vacation_days(self, years, level):
        total = 0

        if years >= 13 and (level == 1):
            total = total + 1
        
        if years >= 14 and (level == 1 or level == 2):
            total = total + 1
        
        if years >= 15 and (level == 1 or level == 2 or level == 3):
            total = total + 1
        
        if years >= 16 and (level == 1 or level == 2 or level == 3 or level == 4):
            total = total + 2
        
        if years >= 17 and (level == 1 or level == 2 or level == 3 or level == 4 or level == 5):
            total = total + 2
        
        if years >= 18 and (level == 1 or level == 2 or level == 3 or level == 4 or level == 5 or level == 6):
            total = total + 2
        
        if years >= 19 and (level == 1 or level == 2 or level == 3 or level == 4 or level == 5 or level == 6 or level == 7):
            total = total + 3
        
        if years >= 20 and (level == 1 or level == 2 or level == 3 or level == 4 or level == 5 or level == 6 or level == 7 or level == 8):
            total = total + 3
        
        if years >= 21 and (level == 1 or level == 2 or level == 3 or level == 4 or level == 5 or level == 6 or level == 7 or level == 8 or level == 9):
            total = total + 3
        
        if years >= 22 and (level == 1 or level == 2 or level == 3 or level == 4 or level == 5 or level == 6 or level == 7 or level == 8 or level == 9 or level == 10):
            total = total + 4

        if years >= 23 and (level == 1 or level == 2 or level == 3 or level == 4 or level == 5 or level == 6 or level == 7 or level == 8 or level == 9 or level == 10 or level == 11):
            total = total + 4

        if years >= 24 and (level == 1 or level == 2 or level == 3 or level == 4 or level == 5 or level == 6 or level == 7 or level == 8 or level == 9 or level == 10 or level == 11 or level == 12):
            total = total + 4

        if years >= 25 and (level == 1 or level == 2 or level == 3 or level == 4 or level == 5 or level == 6 or level == 7 or level == 8 or level == 9 or level == 10 or level == 11 or level == 12 or level == 13):
            total = total + 5

        if years >= 26 and (level == 1 or level == 2 or level == 3 or level == 4 or level == 5 or level == 6 or level == 7 or level == 8 or level == 9 or level == 10 or level == 11 or level == 12 or level == 13 or level == 14):
            total = total + 5

        if years >= 27 and (level == 1 or level == 2 or level == 3 or level == 4 or level == 5 or level == 6 or level == 7 or level == 8 or level == 9 or level == 10 or level == 11 or level == 12 or level == 13 or level == 14 or level == 15):
            total = total + 5

        if years == 0:
            total = 0

        return total

    def get_last_day_of_month(date_str):
        date = datetime.strptime(date_str, '%Y-%m-%d')
        last_day = calendar.monthrange(date.year, date.month)[1]
        last_day_date = datetime(date.year, date.month, last_day)
        return last_day_date.strftime('%Y-%m-%d')

    def extention_contract(date):
        date_dt = datetime.strptime(date, "%Y-%m-%d").date()
        next_month_date = date_dt + relativedelta(months=1)
        return next_month_date.strftime("%Y-%m-%d")