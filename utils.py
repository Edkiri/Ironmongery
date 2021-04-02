# Utils
from datetime import date, datetime, timedelta

# Handle dates.
DATE_FORMAT = "%d-%m-%Y"
TODAY = date.today().strftime(DATE_FORMAT)

def get_weekday(day):
    WEEKDAYS = ("Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo")
    return WEEKDAYS[day.weekday()]


def get_month_name(day_str):
    MONTHS = ("Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre")
    return MONTHS[int(day_str.split('-')[1])-1]


# Handle Float inputs.
def string_to_float(string):
    string = str(string)
    if 'bs' in string:
        string = string.rstrip('bs')
    elif '$' in string:
        string = string.rstrip('$')
    return float(string.replace(',',''))

    
def number_to_str(number):
    number = str(number).replace(',','')
    if "." in number:
        number = float(number)
        if int(str(number).split(".")[1][:2]) > 0:
            if (int(str(number).split(".")[0]) == 0):
                return "{:,.4f}".format(number)
            else:
                return "{:,.2f}".format(number)
        else:
            return "{:,.0f}".format(number)
    else:
        return "{:,}".format(int(number))

def es_casi_igual(num1, num2):
    resta = float(num1) - float(num2)
    if ((resta > 0) and (resta < 0.01)) or (resta == 0):
        return True
    elif (resta < 0) and (resta > -0.01):
        return True
    else:
        return False

def get_summary_payments(payments):
    bs = 0
    usd = 0
    total = 0 
    for payment in payments:
        rate = payment.rate
        if payment.currency == 0:
            if payment.type == 0:  
                bs += payment.amount
                total += (payment.amount / rate)
            else:
                bs -= payment.amount
                total -= (payment.amount / rate)
        else:
            if payment.type == 0:
                usd += payment.amount
                total += payment.amount
            else:
                usd -= payment.amount
                total -= payment.amount
    return (bs, usd, total)