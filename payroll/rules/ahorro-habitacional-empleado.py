from datetime import date, timedelta
import logging
from calendar import monthrange
from dateutil.relativedelta import relativedelta


def condicion_ahorro(today, employee):
    _, r = monthrange(today.year, today.month)
    end_of_month = date(today.year, today.month, r)
    edad = relativedelta(end_of_month, employee.birthday)
    if employee.gender == 'male':
        return edad.years < 60
    else:
        return edad.years < 55




if __name__ == "__main__":

    fmt = (
        "pid %(process)5s [%(asctime)s] "
        + "%(filename)13.13s:%(lineno)4d "
        + "%(levelname)8.8s: %(message)s"
    )

    logging.basicConfig(
        format=fmt, level=logging.DEBUG, datefmt="%Y-%m-%d %H:%M:%S"
    )

    class B:
        pass

    for b,g in [(date(1962,6,5), 'male'), (date(1962,6,6), 'male'),
        (date(1967,6,5), 'male'), (date(1967,6,6), 'female'),
    ]:
        e = B()
        e.birthday = b
        e.gender = g
        today = date.today()
        print(condicion_ahorro(today, e))