from datetime import date, timedelta
import logging
from calendar import monthrange
from dateutil.relativedelta import relativedelta


def calc_provision(payslip, contract):
    _end_date = payslip.date_to
    _, mr = monthrange(_end_date.year, _end_date.month)
    eom = date(_end_date.year, _end_date.month, mr)
    som = date(_end_date.year, _end_date.month, 1)
    eoy = date(_end_date.year, 12, 31)
    y_days = 366 if (_end_date.year % 4 == 0) else 365
    f = min((eoy - contract.date_start).days + 1, y_days) / y_days
    print(f)
    start_date = max(som, contract.date_start)
    c_dias = (eom - start_date).days + 1
    print('c_dias',c_dias)
    u_dias = 60 * c_dias  * f / y_days
    print('u_dias',u_dias)
    return u_dias * contract.wage / 30 


if __name__ == "__main__":

    fmt = (
        "pid %(process)5s [%(asctime)s] "
        + "%(filename)13.13s:%(lineno)4d "
        + "%(levelname)8.8s: %(message)s"
    )

    logging.basicConfig(
        format=fmt, level=logging.DEBUG, datefmt="%Y-%m-%d %H:%M:%S"
    )

    class D:
        pass

    for _d2, _d1 in [
        ("2021-03-31", "2020-01-01"),
        ("2021-03-31", "2021-02-01"),
        ("2021-09-30", "2021-09-15"),
        ("2021-10-31", "2021-09-15"),
    ]:
        y, m, d = _d2.split("-")
        d2 = date(int(y), int(m), int(d))
        y, m, d = _d1.split("-")
        d1 = date(int(y), int(m), int(d))

        p = D()
        p.date_to = d2
        c = D()
        c.wage = 100
        c.date_start = d1
        x = calc_provision(p, c)
        print(x)
 
