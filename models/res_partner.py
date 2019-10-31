# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class AccountInvoice(models.Model):
    _inherit = 'res.partner'

    bussines_field_ids = fields.Many2many(
        comodel_name='res.partner.bussines_field'
    )
