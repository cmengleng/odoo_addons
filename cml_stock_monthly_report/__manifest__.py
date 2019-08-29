# -*- coding: utf-8 -*-
{
    'name': "Stock Monthly Report",

    'summary': """Stock Monthly Report design for Tela Concrete.""",

    'description': """
        Aging report for Concrete Factory
    """,

    'author': "Mengleng Chea",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Generic Modules/Warehouse',
    'version': '12.0.1.0',

    'depends': ['base','purchase','stock','mrp','account','sale_stock',],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
	'images': [],
    'sequence': 1,
    'installable': True,
    'application': True,
    'auto_install': False,
}