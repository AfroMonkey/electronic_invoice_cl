# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ProcurementOrder(models.Model):
    _inherit = 'procurement.order'

    price_unit = fields.Float(
    )
    tax_ids = fields.Many2many(
        comodel_name='account.tax',
    )

    def _get_stock_move_values(self):
        res = super(ProcurementOrder, self)._get_stock_move_values()
        res['price_unit'] = self.price_unit
        res['tax_ids'] = self.tax_ids
        return res
