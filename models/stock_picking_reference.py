# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class StockPickingReference(models.Model):
    _inherit = 'electronic.invoice.reference'
    _name = 'stock.picking.reference'

    picking_id = fields.Many2one(
        comodel_name='stock.picking',
    )
