# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    sequence_id = fields.Many2one(
        comodel_name='ir.sequence',
    )
