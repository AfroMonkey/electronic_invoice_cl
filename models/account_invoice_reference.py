# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class AccountInvoiceReference(models.Model):
    _inherit = 'electronic.invoice.reference'
    _name = 'account.invoice.reference'

    invoice_id = fields.Many2one(
        comodel_name='account.invoice',
    )
