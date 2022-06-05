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
        logging.debug(f"month range: {total}")
        if total not in {28, 29, 30, 31}:
            raise ValueError(f"month range: {total}")
        f = delta.days / total
        logging.debug(f"f={f}")
    else:
        f = 0
    return delta.years, delta.months, f


def dias_vacaciones(payslip, contract):
    def dias_acumulados_al(end_date):
        y, m, f = delta_months(end_date, contract.start_date)
        days = [15]
        for i in range(y):
            days.append(min(16 + i, 30))
        logging.debug(days)
        acc = sum(days[:y])
        last = (m + f) / 12 * days[-1]
        acc += last
        return acc

    _end_date = payslip.end_date
    _, mr = monthrange(_end_date.year, _end_date.month)
    end_date = date(_end_date.year, _end_date.month, mr)
    start_date = end_date - timedelta(days=mr)
    print(end_date, start_date)
    start = dias_acumulados_al(start_date)
    end = dias_acumulados_al(end_date)
    return end - start


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

    contract = B()
    contract.wage = 100
    contract.start_date = date(2015, 4, 17)

    payslip = B()
    payslip.start_date = None

    end_date = date(2022, 2, 28)
    acc = 0
    _end_date = end_date
    for i in range(24):
        payslip.end_date = _end_date
        print(_end_date)
        x = dias_vacaciones(payslip, contract)
        print(x)
        acc += x
        _end_date += relativedelta(months=1)
    print("acc", acc)
