# -*- coding: utf-8 -*-

from odoo import models, fields, api

from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
#========For Excel========
from io import BytesIO
import xlwt
from xlwt import easyxf
import base64
# =====================
class cml_stock_daily_report(models.TransientModel):
    _name = 'cml_stock_daily.report'

    # mytime1 = fields.datetime('Time Method 1', default=lambda self: fields.datetime.now(), required=False, readonly=False, select=True)
    # mytime2 = fields.Datetime('Time Method 2', required="1", default=fields.Datetime.now)

    from_date = fields.Date('From Date', required="1", default=fields.Date.context_today)
    to_date = fields.Date('To Date', required="1", default=fields.Date.context_today)


    company_id = fields.Many2one('res.company', string='Company', required="1", readonly="1", default=lambda self:self.env.user.company_id.id)
    warehouse_ids = fields.Many2many('stock.warehouse', string='Warehouse', required="1", readonly="1", default=lambda self: self.env['stock.warehouse'].search([], limit=1))
    location_ids = fields.Many2one('stock.location', string='Locations')
    excel_file = fields.Binary('Excel File')
    
    # Style of Excel Sheet     
    #==============================
    main_header_style = easyxf('font:height 300;align: vert centre;')
    header_style = easyxf('font:height 200;pattern: pattern solid, fore_color gray25;align: vert centre, horiz center;font: color black; font:bold True;borders: top thin,left thin,right thin,bottom thin')
    left_header_style = easyxf('font:height 200;pattern: pattern solid, fore_color gray25;align: horiz left;font: color black; font:bold True;borders: top thin,left thin,right thin,bottom thin')
    text_left = easyxf('font:height 200; align: horiz left;')
    text_right = easyxf('font:height 200; align: horiz right;', num_format_str='0.000')
    text_left_bold = easyxf('font:height 200; align: horiz right;font:bold True;')
    text_right_bold = easyxf('font:height 200; align: horiz right;font:bold True;', num_format_str='0.000') 
    text_center = easyxf('font:height 200; align: horiz center;')  

    text_left_border = easyxf('font:height 200; align: horiz left;borders: top thin,left thin,right thin,bottom thin;')
    text_right_border = easyxf('font:height 200; align: horiz right;borders: top thin,left thin,right thin,bottom thin;', num_format_str='0.000')
    text_left_bold_border = easyxf('font:height 200; align: horiz right;font:bold True;borders: top thin,left thin,right thin,bottom thin;')
    text_right_bold_border = easyxf('font:height 200; align: horiz right;font:bold True;borders: top thin,left thin,right thin,bottom thin;', num_format_str='0.000') 
    text_center_border = easyxf('font:height 200; align: horiz center;borders: top thin,left thin,right thin,bottom thin;')  
    #==============================  

    @api.multi
    def get_products(self):
        product_pool=self.env['product.product']
        categ_id = self.env['product.category'].search([("name","=","Raw Product")]).id
        return product_pool.search([('categ_id','child_of',categ_id),('type','=','product')])

        # return product_pool.search([('type','=','product')])
                   
    @api.multi
    def create_excel_header(self,worksheet):
        worksheet.write_merge(0, 1, 0, 2, 'Stock Daily Report', self.main_header_style)
        row = 3
        col=0
        worksheet.write(row,col, 'From Date', self.left_header_style)
        date = datetime.strftime(self.from_date, "%d-%m-%Y")
        worksheet.write(row,col+1, date, self.text_left)
        row+=1
        worksheet.write(row,col, 'To Date', self.left_header_style)
        date = datetime.strftime(self.to_date, "%d-%m-%Y")
        worksheet.write(row,col+1, date, self.text_left)
        row+=1
        worksheet.write(row,col, 'Company', self.left_header_style)
        worksheet.write(row,col+1, self.company_id.name or '', self.text_left)
        row+=1
        worksheet.write(row,col, 'Warehouse', self.left_header_style)
        ware_name = ', '.join(map(lambda x: (x.name), self.warehouse_ids))
        worksheet.write(row,col+1,ware_name or '', self.text_left)
        if self.location_ids:
            row+=1
            worksheet.write(row,col, 'Location', self.left_header_style)
            location_name = ', '.join(map(lambda x: (x.name), self.location_ids))
            worksheet.write_merge(row,row, col+1, col+3, location_name or '', self.text_left)
            
        row+=1
        return worksheet, row
        
        
    @api.multi
    def create_table_header(self,worksheet,row,res):
        worksheet.write_merge(row, row+1, 0, 0, 'Code', self.header_style)
        worksheet.write_merge(row,row+1, 1, 1, 'Product', self.header_style)
        worksheet.write_merge(row,row+1, 2, 2, 'Unit', self.header_style)
        worksheet.write_merge(row,row+1, 3, 3, 'Total Qty', self.header_style)
        worksheet.write_merge(row,row+1, 4, 4, 'Total Value', self.header_style)

        worksheet.write_merge(row,row, 5, 6, res['6']['name'], self.header_style)
        worksheet.write(row+1, 5, 'Qunatity', self.header_style)
        worksheet.write(row+1, 6, 'Value', self.header_style)
        worksheet.write_merge(row,row, 7, 8, res['5']['name'], self.header_style)
        worksheet.write(row+1, 7, 'Qunatity', self.header_style)
        worksheet.write(row+1, 8, 'Value', self.header_style)
        worksheet.write_merge(row,row, 9, 10, res['4']['name'], self.header_style)
        worksheet.write(row+1, 9, 'Qunatity', self.header_style)
        worksheet.write(row+1, 10, 'Value', self.header_style)
        worksheet.write_merge(row,row, 11, 12, res['3']['name'], self.header_style)
        worksheet.write(row+1, 11, 'Qunatity', self.header_style)
        worksheet.write(row+1, 12, 'Value', self.header_style)
        worksheet.write_merge(row,row, 13, 14, res['2']['name'], self.header_style)
        worksheet.write(row+1, 13, 'Qunatity', self.header_style)
        worksheet.write(row+1, 14, 'Value', self.header_style)
        worksheet.write_merge(row,row, 15, 16, res['1']['name'], self.header_style)
        worksheet.write(row+1, 15, 'Qunatity', self.header_style)
        worksheet.write(row+1, 16, 'Value', self.header_style)
        worksheet.write_merge(row,row, 17, 18, res['0']['name'], self.header_style)
        worksheet.write(row+1, 17, 'Qunatity', self.header_style)
        worksheet.write(row+1, 18, 'Value', self.header_style)
        row+=1
        return worksheet, row

    @api.multi
    def create_table_header(self,worksheet,row,product_ids,worksheet1):
        r=0
        # for nm in dir(product_ids[0]):
        #     if not nm.startswith('__') and not callable(getattr(product_ids[0], nm)):
        #         worksheet1.write(r,0,nm)
        #         if r>52:
        #             worksheet1.write(r,1,product_ids[0][nm])
        #         r+=1
        # ====================

        # ========================
        worksheet.write_merge(row, row+1, 0, 0, 'Date', self.header_style)
        pro_count = len(product_ids)
        col=1
        worksheet.write_merge(row,row, col, col+pro_count-1, 'Production Usage', self.header_style)
        for product in product_ids:
            worksheet.write(row+1,col,product.name, self.header_style)
            col+=1

        worksheet.write_merge(row,row, col, col+pro_count-1, 'Stock Receipt', self.header_style)
        for product in product_ids:
            worksheet.write(row+1,col,product.name, self.header_style)
            col+=1

        worksheet.write_merge(row,row, col, col+pro_count-1, 'Stock Remaining', self.header_style)
        for product in product_ids:
            worksheet.write(row+1,col,product.name, self.header_style)
            col+=1

        start = self.from_date
        stop = self.to_date
        
        row+=2
        col=pro_count*2
        for product in product_ids:
            pros = self.get_pro_quantity(product,start)
            worksheet.write(row,col+1,pros.qty_available, self.text_left_border)
            col+=1

        while start <= stop:
            col=0
            row+=1
            worksheet.write(row,col,start.strftime('%d-%m-%y'), self.text_center_border)
            start += relativedelta(days=1)
            for product in product_ids:
                pros = self.get_pro_quantity(product,start)
                col+=1
                worksheet.write(row,pro_count*0+col,pros.qty_available, self.text_left_border)
                worksheet.write(row,pro_count*1+col,pros.qty_available, self.text_left_border)
                worksheet.write(row,pro_count*2+col,pros.qty_available, self.text_left_border)

        return worksheet, row
    
    @api.multi
    def get_pro_quantity(self,product,to_date=False):
        if to_date:
            product = product.with_context(to_date=to_date)
        if self.warehouse_ids:
            product = product.with_context(warehouse=self.warehouse_ids.ids)
        product = product.with_context(location=2)
        # if self.location_ids:
        #     product = product.with_context(location=self.location_ids.ids)

        return product

    @api.multi
    def print_excel(self):
        product_ids = self.get_products()

        # Define Wookbook and add sheet 
        workbook = xlwt.Workbook()
        filename = 'Stock Daily.xls'
        worksheet = workbook.add_sheet('Stock Daily')
        worksheet1 = workbook.add_sheet('attr')
        for i in range(0,19):
            if i > 0:
                worksheet.col(i).width = 90 * 30
            else:
                worksheet.col(i).width = 130 * 30

        # Print Excel Header
        worksheet,row = self.create_excel_header(worksheet)
        worksheet,row = self.create_table_header(worksheet,row+2,product_ids,worksheet1)
        #download Excel File
        fp = BytesIO()
        workbook.save(fp)
        fp.seek(0)
        excel_file = base64.encodestring(fp.read())
        fp.close()
        self.write({'excel_file': excel_file})

        if self.excel_file:
            active_id = self.ids[0]
            return {
                'type': 'ir.actions.act_url',
                'url': 'web/content/?model=cml_stock_daily.report&download=true&field=excel_file&id=%s&filename=%s' % (
                    active_id, filename),
                'target': 'new',
            }
    
        
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: