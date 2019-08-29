# -*- coding: utf-8 -*-
from odoo import http

# class CmlStockMonthlyReport(http.Controller):
#     @http.route('/cml_stock_monthly_report/cml_stock_monthly_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cml_stock_monthly_report/cml_stock_monthly_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cml_stock_monthly_report.listing', {
#             'root': '/cml_stock_monthly_report/cml_stock_monthly_report',
#             'objects': http.request.env['cml_stock_monthly_report.cml_stock_monthly_report'].search([]),
#         })

#     @http.route('/cml_stock_monthly_report/cml_stock_monthly_report/objects/<model("cml_stock_monthly_report.cml_stock_monthly_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cml_stock_monthly_report.object', {
#             'object': obj
#         })