# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class AccountTax(models.Model):
    _inherit = 'account.tax'

    code = fields.Char(
        size=4,
        required=True,
    )
