# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class StockMove(models.Model):
    _inherit = 'stock.move'

    price_unit = fields.Float(
    )
    tax_ids = fields.Many2many(
        comodel_name='account.tax',
    )
    amount_untaxed = fields.Float(
        compute='_get_amount_untaxed'
    )
    amount_tax = fields.Float(
        compute='_get_amount_tax'
    )
    amount_total = fields.Float(
        compute='_get_amount_total'
    )

    @api.depends('product_qty', 'price_unit')
    def _get_amount_untaxed(self):
        for record in self:
            record.amount_untaxed = record.product_qty * record.price_unit

    @api.depends('amount_untaxed', 'tax_ids')
    def _get_amount_tax(self):
        for record in self:
            record.amount_tax = sum(tax.amount * record.amount_untaxed / 100 for tax in record.tax_ids)

    @api.depends('amount_untaxed', 'amount_tax')
    def _get_amount_total(self):
        for record in self:
            record.amount_total = record.amount_untaxed + record.amount_tax
