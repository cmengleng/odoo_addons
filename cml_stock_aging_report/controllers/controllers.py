# -*- coding: utf-8 -*-
from odoo import http

# class CmlStockAgingReport(http.Controller):
#     @http.route('/cml_stock_aging_report/cml_stock_aging_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cml_stock_aging_report/cml_stock_aging_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cml_stock_aging_report.listing', {
#             'root': '/cml_stock_aging_report/cml_stock_aging_report',
#             'objects': http.request.env['cml_stock_aging_report.cml_stock_aging_report'].search([]),
#         })

#     @http.route('/cml_stock_aging_report/cml_stock_aging_report/objects/<model("cml_stock_aging_report.cml_stock_aging_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cml_stock_aging_report.object', {
#             'object': obj
#         })