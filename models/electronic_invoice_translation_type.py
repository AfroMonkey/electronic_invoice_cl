# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ElectronicInvoiceTranslationType(models.Model):
    _inherit = 'basic_code_desc_model'
    _name = 'electronic_invoice.translation_type'
