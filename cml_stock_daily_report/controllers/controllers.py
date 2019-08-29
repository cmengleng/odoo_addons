# -*- coding: utf-8 -*-
from odoo import http

# class CmlStockDailyReport(http.Controller):
#     @http.route('/cml_stock_daily_report/cml_stock_daily_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cml_stock_daily_report/cml_stock_daily_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cml_stock_daily_report.listing', {
#             'root': '/cml_stock_daily_report/cml_stock_daily_report',
#             'objects': http.request.env['cml_stock_daily_report.cml_stock_daily_report'].search([]),
#         })

#     @http.route('/cml_stock_daily_report/cml_stock_daily_report/objects/<model("cml_stock_daily_report.cml_stock_daily_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cml_stock_daily_report.object', {
#             'object': obj
#         })