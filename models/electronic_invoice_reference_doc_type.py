# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ElectronicInvoiceReferenceDocType(models.Model):
    _inherit = 'basic_code_desc_model'
    _name = 'electronic_invoice.reference_doc_type'
