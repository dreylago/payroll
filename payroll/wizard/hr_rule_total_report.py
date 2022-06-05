from odoo import _, fields, models, api
from odoo.exceptions import UserError
import logging
from collections import defaultdict, Counter
from ..models.utils import display_table


class HrRuleTotalReport(models.TransientModel):
    _name = "hr.rule.total.report"
    _description = "Reporte reglas de Salario"

    date_from = fields.Date(string="Desde")
    date_to = fields.Date(string="Hasta")
    report_details = fields.Html(string="Details", copy=False)

    def get_html_report(self):
        self.report_details = self._get_html_report(self.date_from, self.date_to, self.env.company)

    def erase_report(self):
        self.report_details = ''

    @api.onchange('date_from', 'date_to')
    def _erase_report(self):
        self.report_details = ''

    def _get_html_report(self, date_from, date_to, company):
        res = self.calc_report(date_from, date_to, company.id)
        html = self.format_report(res)
        header = self.report_header(date_from, date_to, company.name)
        return header + '<br/>' + html 
    
    def format_report(self, data):
        keys = sorted(data.keys(), key=lambda x: x[4])
        rows = []
        types = ["ASG", "DED", "APT", "PRV"]
        totals = [0] * len(types)
        for key in keys:
            total = data[key]
            code, name, cat, cat_type, seq = key
            row = [code, name]
            cols = [""] * len(types)
            try:
                pos = types.index(cat_type)
                cols[pos] = f"{total:,.2f}"
                totals[pos] += total
            except ValueError:
                pass
            row += cols
            rows.append(row)

        total_row = ["", "Totales"]
        for t in totals:
            total_row.append(f"{t:,.2f}")

        headers = [
            "Código",
            "Descripción",
            "Asignaciones",
            "Deducciones",
            "Aportes",
            "Previsión",
        ]
        header_style = (
            "background-color: #ddd; "
            "text-align:right; "
            "padding: 0.1em; "
            "min-width: 12em"
        )
        return display_table(
            rows, headers, header_style=header_style, footer=total_row
        )


    def report_header(self, date_from, date_to, company_name):
        headers = ["Reporte", "Compañía", "Desde", "Hasta"]
        rows = []
        rows.append(["Líneas de Nómina"])
        rows.append([company_name])
        rows.append([date_from])
        rows.append([date_to])
        header_table = display_table(rows, left_header=headers)
        return header_table

    def calc_report(self, date_from, date_to, company_id):
        rows = self.env["hr.payslip"].search(
            [
                "&",
                ("date_from", ">=", date_from),
                "&",
                ("date_to", "<=", date_to),
                ("company_id", "=", company_id),
            ]
        )
        data = Counter()
        for row in rows:
            for line in row.line_ids:
                rule = line.salary_rule_id
                cat = rule.category_id.code
                cat_type = rule.category_id.parent_id.code or cat
                if cat_type in {"ASG", "DED", "PRV"}:
                    total = line.total
                    if row.credit_note:
                        total = -total
                    data[
                        (rule.code, rule.name, cat, cat_type, rule.sequence)
                    ] += total

        return data
