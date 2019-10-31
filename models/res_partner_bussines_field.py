# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class RespartnerBussinesField(models.Model):
    _name = 'res.partner.bussines_field'

    name = fields.Char(
        compute='_get_name',
        store=True,
    )
    code = fields.Char(
    )
    desc = fields.Char(
    )

    @api.depends('code', 'desc')
    def _get_name(self):
        for record in self:
            record.name = u'{} - {}'.format(record.code, record.desc)
