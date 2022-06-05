from datetime import date, timedelta
import logging
from calendar import monthrange
from dateutil.relativedelta import relativedelta


def delta_months(end_date, start_date):
    delta = relativedelta(end_date + timedelta(days=1), start_date)
    if delta.days > 0:
        next_end = start_date + relativedelta(
            years=delta.years, months=delta.months + 1, days=-1
        )
        remain = (next_end - end_date).days
        total = delta.days + remain
        f = delta.days / total
    else:
        f = 0
    return delta.years, delta.months, f

def dias_acumulados_al(end_date, start_date):
    y, m, f = delta_months(end_date, start_date)
    days = [15]
    for i in range(y):
        days.append(min(days[0] + 1 + i, 30))
    acc = sum(days[:y])
    last = (m + f) / 12 * days[-1]
    acc += last
    return acc

def dias_vacaciones(payslip, contract):
    _end_date = payslip.date_to
    _, mr = monthrange(_end_date.year, _end_date.month)
    end_date = date(_end_date.year, _end_date.month, mr)
    start_date = end_date - timedelta(days=mr)
    start = dias_acumulados_al(start_date, contract.date_start)
    end = dias_acumulados_al(end_date, contract.date_start)
    return end - start


def calc(payslip, contract):
    dias = dias_vacaciones(payslip, contract)
    return dias * contract.wage / 30 


if __name__ == "__main__":

    fmt = (
        "pid %(process)5s [%(asctime)s] "
        + "%(filename)13.13s:%(lineno)4d "
        + "%(levelname)8.8s: %(message)s"
    )

    logging.basicConfig(
        format=fmt, level=logging.DEBUG, datefmt="%Y-%m-%d %H:%M:%S"
    )

    for _d2, _d1 in [
        ("2000-03-31", "2000-01-01"),
        ("2000-04-01", "2000-01-01"),
        ("2000-03-30", "2000-01-02"),
        ("2000-03-31", "2000-01-02"),
        ("2000-04-01", "2000-01-02"),
        ("2000-04-02", "2000-01-02"),
        ("2000-02-28", "2000-01-02"),
        ("2000-02-29", "2000-01-02"),
        ("2000-03-01", "2000-01-02"),
        ("2000-03-02", "2000-01-02"),
        ("2001-02-26", "2000-01-02"),
        ("2001-02-27", "2000-01-02"),
        ("2001-02-28", "2000-01-02"),
        ("2001-03-01", "2000-01-02"),
        ("2001-03-02", "2000-01-02"),
    ]:
        y, m, d = _d2.split("-")
        d2 = date(int(y), int(m), int(d))
        y, m, d = _d1.split("-")
        d1 = date(int(y), int(m), int(d))
        print("====================")
        print("from", d2, "to", d1)
        print(delta_months(d2, d1))
        print(relativedelta(d2 + relativedelta(days=1), d1))
        print((d2 + timedelta(days=1) - d1).days)

    class B:
        pass

    c = B()
    c.wage = 100
    c.start_date = date(2015, 4, 17)

    p = B()
    p.start_date = None

    end_date = date(2022, 2, 28)
    acc = 0
    _end_date = end_date
    for i in range(24):
        p.date_to = _end_date
        print(_end_date)
        y = calc(p, c)
        print(y)
        x = dias_vacaciones(p, c)
        print(x)
        acc += x
        _end_date += relativedelta(months=1)
    print("acc", acc)
