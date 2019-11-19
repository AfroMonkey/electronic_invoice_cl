# -*- coding: utf-8 -*-

from datetime import timedelta, datetime
from unidecode import unidecode  # pip install unidecode
from collections import OrderedDict
from base64 import encodestring
from zeep import Client  # pip install zeep

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError

from electronic_invoice_api import get_xml, send_xml


DATE_FORMAT = '%d-%m-%Y'
DESPATCH_DOC = 52


def dict_string(d):
    for key in d:
        if type(d[key]) == unicode:
            d[key] = unidecode(d[key] or '')
        d[key] = str(d[key] or '')
    return d


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
    reference_ids = fields.One2many(
        comodel_name='account.invoice.reference',
        inverse_name='invoice_id',
    )
    electronic_invoice_xml = fields.Binary(
        attachment=True,
        copy=False,
        readonly=True,
        string=_('XML')
    )
    fname_electronic_invoice_xml = fields.Char(
        compute='_get_fname_electronic_invoice_xml'
    )
    ei_error_code = fields.Char(
        readonly=True,
        copy=False,
    )
    ei_status = fields.Char(
        copy=False,
        readonly=True,
        string=_('Status')
    )
    ei_pdf = fields.Char(
        copy=False,
        readonly=True,
        string=_('PDF')
    )
    ei_ring = fields.Char(
        copy=False,
        readonly=True,
        string=_('Ring')
    )

    @api.depends('partner_id')
    def _get_bussines_field(self):
        for record in self:
            partner_id = self.partner_id.parent_id or self.partner_id
            if partner_id and partner_id.bussines_field_ids:
                record.bussines_field_id = partner_id.bussines_field_ids[0]

    @api.depends('number')
    def _get_fname_electronic_invoice_xml(self):
        for record in self:
            if record.electronic_invoice_xml:
                if record.number:
                    record.fname_electronic_invoice_xml = '{}.xml'.format(record.number)
                else:
                    record.fname_electronic_invoice_xml = '{} {}.xml'.format(record.partner_id.vat, record.date_invoice)

    def _get_data(self):
        partner_id = self.partner_id.parent_id or self.partner_id
        data = OrderedDict()
        data['Tipo'] = self.journal_id.code[:-1]
        data['Folio'] = self.journal_id.sequence_id.next_by_id()
        date_invoice = datetime.strptime(self.date_invoice, '%Y-%m-%d')
        date_invoice = datetime.strftime(date_invoice, DATE_FORMAT)
        data['FechaEmision'] = date_invoice
        date_due = datetime.strptime(self.date_invoice, '%Y-%m-%d')
        date_due += timedelta(days=self.payment_term_id.line_ids[0].days)
        date_due = datetime.strftime(date_due, DATE_FORMAT)
        data['FechaVencimiento'] = date_due
        data['FormaPago'] = 1 if self.payment_term_id.line_ids[0].days == 0 else 2
        data['GlosaPago'] = self.payment_term_id.name
        data['Sucursal'] = self.sucursal
        data['Vendedor'] = self.user_id.name
        if not partner_id or not partner_id.vat:
            raise ValidationError(_('Partner must have VAT.'))
        data['ReceptorRut'] = '{}-{}'.format(partner_id.vat[2:-1], partner_id.vat[-1:])
        data['ReceptorRazon'] = partner_id.name  # TODO company
        data['ReceptorGiro'] = self.bussines_field_id.desc
        data['ReceptorContacto'] = self.partner_id.name
        print(self.partner_id.name)
        data['ReceptorDireccion'] = partner_id.street
        data['ReceptorComuna'] = partner_id.street2
        data['ReceptorCiudad'] = partner_id.city
        data['ReceptorFono'] = partner_id.phone or partner_id.mobile
        data['Unitarios'] = 1
        exento = sum(line.price_subtotal for line in self.invoice_line_ids if not line.invoice_line_tax_ids)
        data['Neto'] = self.amount_untaxed - exento
        data['Exento'] = exento
        data['Iva'] = round(self.amount_tax)
        data['Total'] = round(self.amount_total)
        dict_string(data)
        return data

    def _get_references(self):
        references = []
        for i, reference in enumerate(self.reference_ids, start=1):
            references.append(dict_string({
                'RefNroLin': i,
                'RefCodigo': reference.name.code,
                'RefMotivo': reference.RefMotivo,
                'RefFolio': reference.RefFolio,
                'RefFecha': datetime.strftime(datetime.strptime(reference.RefFecha, '%Y-%m-%d'), DATE_FORMAT),
                'RefRazon': reference.RefRazon,
            }))
        return references

    def _get_details(self):
        details = []
        for i, line in enumerate(self.invoice_line_ids, start=1):
            ir_values_obj = self.env['ir.values']
            default_taxes = ir_values_obj.get_default('product.template', "taxes_id", company_id=self.company_id.id)
            filtered_taxes = line.invoice_line_tax_ids.filtered(lambda line: line.id not in default_taxes)
            details.append(dict_string({
                'NrLinDetalle': i,
                'Codigo': line.product_id.default_code,
                'Descripcion': line.product_id.name,
                'Glosa': line.name,
                'Cantidad': line.quantity,
                'UnidadMedida': line.uom_id.code,
                'IndExento': 'NO' if line.invoice_line_tax_ids else 'SI',
                'Unitario': line.price_unit,
                'DescuentoLinea': '$',  # TODO check
                'ValorDescuento': line.discount * line.price_subtotal,  # TODO check
                'SubTotal': line.price_subtotal,
                # TODO second stage 'BrutoxBotella': line.,
                'ImptoCodigo': filtered_taxes.code if line.invoice_line_tax_ids else '',
                'ImptoTaza': filtered_taxes.amount if line.invoice_line_tax_ids else '',
                'ImptoMonto': round(filtered_taxes.amount / 100 * line.price_subtotal) if line.invoice_line_tax_ids else '',
            }))
        return details

    @api.multi
    def send_xml(self):
        data = self._get_data()
        references = self._get_references()
        details = self._get_details()
        xml_string = get_xml(data, references, details)
        self.electronic_invoice_xml = encodestring(xml_string)
        response = send_xml(
            url=self.company_id.ei_url,
            user=self.company_id.ei_user,
            password=self.company_id.ei_password,
            id_user=self.company_id.ei_id_user,
            id_company=self.company_id.ei_id_company,
            environment=self.company_id.ei_environment,
            ringing=self.company_id.ei_ringing,
            xml_string=xml_string
        )
        self.ei_error_code = response[0]
        self.ei_status = response[3]
        if self.ei_error_code == '0':
            self.action_invoice_open()
        else:
            return  # TODO log
        self.number = response[2]
        self.ei_pdf = response[4]
        self.ei_ring = response[5]
