# -*- coding: utf-8 -*-

from datetime import timedelta, datetime

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

from xml_generator import get_xml


DATE_FORMAT = '%d-%m-%Y'


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    bussines_field_id = fields.Many2one(
        comodel_name='res.partner.bussines_field',
        compute='_get_bussines_field',
        store=True,
        readonly=False,
    )
    sucursal = fields.Char(
    )
    TransPatente = fields.Char(
        string=_('Patente'),
    )
    TransRutChofer = fields.Char(
        string=_('RUT'),
    )
    TransNombreChofer = fields.Char(
        string=_('Nombre'),
    )
    TransDireccionDestino = fields.Char(
        string=_('Dirección'),
    )
    TransComunaDestino = fields.Char(
        string=_('Comuna'),
    )
    TransCiudadDestino = fields.Char(
        string=_('Ciudad'),
    )

    @api.depends('partner_id')
    def _get_bussines_field(self):
        for record in self:
            if record.partner_id and record.partner_id.bussines_field_ids:
                record.bussines_field_id = record.partner_id.bussines_field_ids[0]

    @api.multi
    def send_xml(self):
        data = {}
        data['Tipo'] = 'TODO'  # TODO
        data['Folio'] = self.id
        date_invoice = datetime.strptime(self.date_invoice, '%Y-%m-%d')
        date_invoice = datetime.strftime(date_invoice, DATE_FORMAT)
        data['FechaEmision'] = date_invoice
        date_due = datetime.strptime(self.date_invoice, '%Y-%m-%d')
        date_due += timedelta(days=self.payment_term_id.line_ids[0].days)
        date_due = datetime.strftime(date_due, DATE_FORMAT)
        data['FechaVencimiento'] = date_due
        data['TipoDespacho'] = 'TODO'  # TODO
        data['TipoTraslado'] = 'TODO'  # TODO
        data['FormaPago'] = 1 if self.payment_term_id.line_ids[0].days == 0 else 2
        data['GlosaPago'] = 'TODO'  # TODO payment_term_id.line_ids[0].name doesn't exist
        data['Sucursal'] = self.sucursal
        data['Vendedor'] = self.user_id.name
        data['ReceptorRut'] = 'TODO'  # TODO self.partner_id.company_id.vat[2:] COMPANY?
        data['ReceptorRazon'] = 'TODO'  # TODO self.partner_id.company_id.name COMPANY?
        data['ReceptorGiro'] = self.bussines_field_id.desc
        data['ReceptorContacto'] = self.partner_id.name
        data['ReceptorDireccion'] = self.partner_id.street
        data['ReceptorComuna'] = self.partner_id.street2
        data['ReceptorCiudad'] = self.partner_id.city
        data['ReceptorFono'] = self.partner_id.phone or partner_id.mobile
        data['TransPatente'] = self.TransPatente
        data['TransRutChofer'] = self.TransRutChofer
        data['TransNombreChofer'] = self.TransNombreChofer
        data['TransDireccionDestino'] = self.TransDireccionDestino
        data['TransComunaDestino'] = self.TransComunaDestino
        data['TransCiudadDestino'] = self.TransCiudadDestino
        data['Unitarios'] = 1
        exento = sum(line.price_subtotal for line in self.invoice_line_ids if not line.invoice_line_tax_ids)
        data['Neto'] = self.amount_untaxed - exento
        data['Exento'] = exento
        data['Iva'] = self.amount_tax
        data['Total'] = self.amount_total
        for key in data:
            data[key] = str(data[key])
        get_xml(data)
