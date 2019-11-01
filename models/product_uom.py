# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ProductUOM(models.Model):
    _inherit = 'product.uom'

    code = fields.Char(
        size=4,
        required=True,
    )
