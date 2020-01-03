# -*- coding: utf-8 -*-

from datetime import timedelta, datetime
from collections import OrderedDict

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError

from electronic_invoice_api import dict_string, DATE_FORMAT


class StockPicking(models.Model):
    _name = 'stock.picking'
    _inherit = ['stock.picking', 'electronic_invoice']

    journal_id = fields.Many2one(
        comodel_name='account.journal',
    )
    despatch_type_id = fields.Many2one(
        comodel_name='electronic_invoice.despatch_type',
    )
    translation_type_id = fields.Many2one(
        comodel_name='electronic_invoice.translation_type',
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
    )
    amount_untaxed = fields.Float(
        compute='_get_amounts',
    )
    amount_tax = fields.Float(
        compute='_get_amounts',
    )
    amount_total = fields.Float(
        compute='_get_amounts',
    )
    trans_plates = fields.Char(
    )
    trans_driver_vat = fields.Char(
    )
    trans_driver_name = fields.Char(
    )
    trans_destination_address = fields.Char(
    )
    trans_destination_commune = fields.Char(
    )
    trans_destination_city = fields.Char(
    )

    @api.depends('move_lines')
    def _get_amounts(self):
        for record in self:
            record.amount_untaxed = sum(line.amount_untaxed for line in record.move_lines)
            record.amount_tax = sum(line.amount_tax for line in record.move_lines)
            record.amount_total = sum(line.amount_total for line in record.move_lines)

    @api.depends('name')
    def _get_fname_electronic_invoice_xml(self):
        for record in self:
            if record.electronic_invoice_xml:
                record.fname_electronic_invoice_xml = '{}.xml'.format(record.name)

    def _get_data(self):
        partner_id = self.partner_id.parent_id or self.partner_id
        data = OrderedDict()
        data['Tipo'] = self.journal_id.code[:-1]
        data['Folio'] = self.journal_id.sequence_id.next_by_id()
        min_date = datetime.strptime(self.min_date, '%Y-%m-%d %H:%M:%S')
        min_date = datetime.strftime(min_date, DATE_FORMAT)
        data['FechaEmision'] = min_date
        data['FechaVencimiento'] = min_date
        data['TipoDespacho'] = self.despatch_type_id.code
        data['TipoTraslado'] = self.translation_type_id.code
        data['FormaPago'] = ''  # TODO check
        data['GlosaPago'] = ''
        data['Sucursal'] = self.sucursal
        data['Vendedor'] = self.user_id.name
        if not partner_id or not partner_id.vat:
            raise ValidationError(_('Partner must have VAT.'))
        data['ReceptorRut'] = '{}-{}'.format(partner_id.vat[2:-1], partner_id.vat[-1:])
        data['ReceptorRazon'] = partner_id.name
        data['ReceptorGiro'] = self.bussines_field_id.desc
        data['ReceptorContacto'] = self.partner_id.name
        data['ReceptorDireccion'] = partner_id.street
        data['ReceptorComuna'] = partner_id.street2
        data['ReceptorCiudad'] = partner_id.city
        data['ReceptorFono'] = partner_id.phone or partner_id.mobile
        data['TransPatente'] = self.trans_plates
        data['TransRutChofer'] = self.trans_driver_vat
        data['TransNombreChofer'] = self.trans_driver_name
        data['TransDireccionDestino'] = self.trans_destination_address
        data['TransComunaDestino'] = self.trans_destination_commune
        data['TransCiudadDestino'] = self.trans_destination_city
        data['Unitarios'] = 1
        data['Neto'] = round(self.amount_untaxed)
        data['Exento'] = ''
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
        for i, line in enumerate(self.move_lines, start=1):
            ir_values_obj = self.env['ir.values']
            default_taxes = ir_values_obj.get_default('product.template', "taxes_id", company_id=self.company_id.id)
            filtered_taxes = line.tax_ids.filtered(lambda line: line.id not in default_taxes)
            details.append(dict_string({
                'NrLinDetalle': i,
                'Codigo': line.product_id.default_code,
                'Descripcion': line.product_id.name,
                'Glosa': line.name,
                'Cantidad': line.product_uom_qty,
                'UnidadMedida': line.product_uom.code,
                'IndExento': 'NO' if line.tax_ids else 'SI',
                'Unitario': line.price_unit,
                'DescuentoLinea': '$',  # TODO check
                'ValorDescuento': '',  # TODO check
                'SubTotal': line.amount_untaxed,
                # TODO 'BrutoxBotella'
                'ImptoCodigo': filtered_taxes.code if line.tax_ids else '',
                'ImptoTaza': filtered_taxes.amount if line.tax_ids else '',
                'ImptoMonto': round(filtered_taxes.amount / 100 * line.amount_untaxed) if line.tax_ids else '',
            }))
        return details

    @api.multi
    def send_xml(self):
        response = super(StockPicking, self).send_xml()
