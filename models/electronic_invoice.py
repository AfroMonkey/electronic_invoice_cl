# -*- coding: utf-8 -*-

from base64 import encodestring

from odoo import api, fields, models, _

from electronic_invoice_api import get_xml, send_xml


class ElectronicInvoice(models.AbstractModel):
    _name = 'electronic_invoice'

    bussines_field_id = fields.Many2one(
        comodel_name='res.partner.bussines_field',
        compute='_get_bussines_field',
        store=True,
        readonly=False,
    )
    sucursal = fields.Char(
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
            partner_id = record.partner_id.parent_id or record.partner_id
            if partner_id and partner_id.bussines_field_ids:
                record.bussines_field_id = partner_id.bussines_field_ids[0]

    def _get_fname_electronic_invoice_xml(self):
        raise NotImplementedError(_('In order to use _get_fname_electronic_invoice_xml the method must be implemented'))

    def _get_data(self):
        raise NotImplementedError(_('In order to use _get_data the method must be implemented'))

    def _get_references(self):
        raise NotImplementedError(_('In order to use _get_references the method must be implemented'))

    def _get_references(self):
        raise NotImplementedError(_('In order to use _get_references the method must be implemented'))

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
            xml_string=xml_string,
            folio=data['Folio']
        )
        self.ei_error_code = response[0]
        self.ei_status = response[3]
        if self.ei_error_code == '0':
            self.ei_pdf = response[4]
            self.ei_ring = response[5]
        return response
