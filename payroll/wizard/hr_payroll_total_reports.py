class HrPayrollTotalReport(models.TransientModel):
    _name = "hr.payroll.total.report"
    _description = "Payroll total report"

    date_from = fields.Date(string='From Date')
    date_to = fields.Date(string='To Date')
