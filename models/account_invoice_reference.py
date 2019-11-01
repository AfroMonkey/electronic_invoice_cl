# -*- coding: utf-8 -*-

from unidecode import unidecode  # pip install unidecode

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountInvoiceReference(models.Model):
    _name = 'account.invoice.reference'

    invoice_id = fields.Many2one(
        comodel_name='account.invoice',
    )
    name = fields.Many2one(
        comodel_name='electronic_invoice.reference_doc_type',
        string=_('Código')
    )
    RefMotivo = fields.Selection(
        selection=[
            (1, 'Anulación'),
            (2, 'Corrección texto'),
            (3, 'Corrección monto'),
        ],
        string=_('Motivo'),
    )
    RefFolio = fields.Char(
        required=True,
        string=_('Folio'),
    )
    RefFecha = fields.Date(
        required=True,
        string=_('Fecha'),
    )
    RefRazon = fields.Text(
        size=90,
        required=True,
        string=_('Razón'),
    )

    @api.constrains('RefMotivo', 'name')
    def _check_RefMotivo(self):
        for record in self:
            if record.RefMotivo == 2 and record.name.code != '61':
                raise ValidationError(_('{} can not have that reason'.format(unidecode(record.name.desc))))
