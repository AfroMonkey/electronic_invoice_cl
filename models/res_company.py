# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ResCompany(models.Model):
    _inherit = 'res.company'

    ei_url = fields.Char(
        required=True,
        string=_('URL')
    )
    ei_user = fields.Char(
        required=True,
        string=_('User')
    )
    ei_password = fields.Char(
        required=True,
        string=_('Password')
    )
    ei_id_user = fields.Char(
        required=True,
        string=_('Id User')
    )
    ei_id_company = fields.Char(
        required=True,
        string=_('Id Company')
    )
    ei_environment = fields.Char(
        required=True,
        string=_('Environment')
    )
    ei_ringing = fields.Char(
        required=True,
        string=_('Ringing')
    )
