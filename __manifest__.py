# -*- coding: utf-8 -*-

{
    'name': 'Electronic Invoice Chile',
    'version': '1.14.1',
    'author': 'Navarro Moisés',
    'website': 'https://github.com/AfroMonkey/electronic_invoice_cl',
    'category': 'Localization',
    'depends': [
        'account',
        'account_accountant',
        'stock',
        'sale',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence.xml',
        'data/account_journal.xml',
        'data/electronic_invoice_despatch_type.xml',
        'data/electronic_invoice_reference_doc_type.xml',
        'data/electronic_invoice_translation_type.xml',
        'data/res_partner_bussines_field.xml',
        'views/account_invoice.xml',
        'views/account_journal.xml',
        'views/account_tax.xml',
        'views/product_uom.xml',
        'views/res_company.xml',
        'views/res_partner.xml',
        'views/stock_move.xml',
        'views/stock_picking.xml',
    ],
    'external_dependencies': {
        'python': [
            'unidecode',  # pip install unidecode
            'zeep',  # pip install zeep
        ]
    }
}
