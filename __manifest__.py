# -*- coding: utf-8 -*-

{
    'name': 'Electronic Invoice Chile',
    'version': '0.1.0',
    'author': 'Navarro Moisés',
    'website': 'https://github.com/AfroMonkey/electronic_invoice_cl',
    'category': 'Localization',
    'depends': [
        'account',
        'account_accountant',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/res_partner_bussines_field.xml',
        'views/account_invoice.xml',
        'views/res_partner.xml',
    ],
}
