# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ElectronicInvoiceDespatchType(models.Model):
    _inherit = 'basic_code_desc_model'
    _name = 'electronic_invoice.despatch_type'
