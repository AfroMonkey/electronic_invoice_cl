from lxml import etree
from unidecode import unidecode  # pip install unidecode
from zeep import Client

import logging

_logger = logging.getLogger(__name__)


DATE_FORMAT = '%d-%m-%Y'
DESPATCH_DOC = '52'  # TODO ref


def dict_string(d):
    for key in d:
        if type(d[key]) == unicode:
            d[key] = unidecode(d[key] or '')
        d[key] = str(d[key] or '')
    return d


def insert(parent, child, text=""):
    child = etree.Element(child)
    child.text = text
    parent.append(child)


def _process_data(DTE, data):
    insert(DTE, 'Tipo', data['Tipo'])
    insert(DTE, 'Folio', data['Folio'])
    insert(DTE, 'FechaEmision', data['FechaEmision'])
    insert(DTE, 'FechaVencimiento', data['FechaVencimiento'])
    if data['Tipo'] == DESPATCH_DOC:
        insert(DTE, 'TipoDespacho', data['TipoDespacho'])
        insert(DTE, 'TipoTraslado', data['TipoTraslado'])
    insert(DTE, 'FormaPago', data['FormaPago'])
    insert(DTE, 'GlosaPago', data['GlosaPago'])
    insert(DTE, 'Sucursal', data['Sucursal'])
    insert(DTE, 'Vendedor', data['Vendedor'])
    insert(DTE, 'ReceptorRut', data['ReceptorRut'])
    insert(DTE, 'ReceptorRazon', data['ReceptorRazon'])
    insert(DTE, 'ReceptorGiro', data['ReceptorGiro'])
    insert(DTE, 'ReceptorContacto', data['ReceptorContacto'])
    insert(DTE, 'ReceptorDireccion', data['ReceptorDireccion'])
    insert(DTE, 'ReceptorComuna', data['ReceptorComuna'])
    insert(DTE, 'ReceptorCiudad', data['ReceptorCiudad'])
    insert(DTE, 'ReceptorFono', data['ReceptorFono'])
    if data['Tipo'] == DESPATCH_DOC:
        insert(DTE, 'TransPatente', data['TransPatente'])
        insert(DTE, 'TransRutChofer', data['TransRutChofer'])
        insert(DTE, 'TransNombreChofer', data['TransNombreChofer'])
        insert(DTE, 'TransDireccionDestino', data['TransDireccionDestino'])
        insert(DTE, 'TransComunaDestino', data['TransComunaDestino'])
        insert(DTE, 'TransCiudadDestino', data['TransCiudadDestino'])
    insert(DTE, 'Unitarios', data['Unitarios'])
    insert(DTE, 'Neto', data['Neto'])
    insert(DTE, 'Exento', data['Exento'])
    insert(DTE, 'Iva', data['Iva'])
    insert(DTE, 'Total', data['Total'])


def _process_references(DTE, references):
    for reference in references:
        reference_child = etree.Element("Referencias")
        insert(reference_child, "RefNroLin", reference['RefNroLin'])
        insert(reference_child, "RefCodigo", reference['RefCodigo'])
        insert(reference_child, "RefMotivo", reference['RefMotivo'])
        insert(reference_child, "RefFolio", reference['RefFolio'])
        insert(reference_child, "RefFecha", reference['RefFecha'])
        insert(reference_child, "RefRazon", reference['RefRazon'])
        DTE.append(reference_child)


def _process_details(DTE, details):
    for detail in details:
        detail_child = etree.Element("Detalle")
        insert(detail_child, "NrLinDetalle", detail['NrLinDetalle'])
        insert(detail_child, "Codigo", detail['Codigo'])
        insert(detail_child, "Descripcion", detail['Descripcion'])
        insert(detail_child, "Glosa", detail['Glosa'])
        insert(detail_child, "Cantidad", detail['Cantidad'])
        insert(detail_child, "UnidadMedida", detail['UnidadMedida'])
        insert(detail_child, "IndExento", detail['IndExento'])
        insert(detail_child, "Unitario", detail['Unitario'])
        insert(detail_child, "DescuentoLinea", detail['DescuentoLinea'])
        insert(detail_child, "ValorDescuento", detail['ValorDescuento'])
        insert(detail_child, "SubTotal", detail['SubTotal'])
        # TODO insert(detail_child, "BrutoxBotella", detail['BrutoxBotella'])
        insert(detail_child, "ImptoCodigo", detail['ImptoCodigo'])
        insert(detail_child, "ImptoTaza", detail['ImptoTaza'])
        insert(detail_child, "ImptoMonto", detail['ImptoMonto'])
        DTE.append(detail_child)


def get_xml(data, references, details):
    DTE = etree.Element('DTE', version='1.0')
    _process_data(DTE, data)
    _process_references(DTE, references)
    _process_details(DTE, details)
    _logger.info('XML for {} invoice created'.format(data['Folio']))
    return '<?xml version="1.0" encoding="UTF-8"?>' + etree.tostring(DTE, pretty_print=True)


def send_xml(url, user, password, id_user, id_company, environment, ringing, xml_string):
    client = Client(url)

    res = client.service.recibexml(
        xml_string,
        user,
        password,
        id_user,
        id_company,
        environment,
        ringing,
    )
    res = res.split('|')
    if res[0] == '0':
        _logger.info('Electronic Invoice Success: {}'.format(res))
    else:
        _logger.error('Electronic Invoice Failed: {}'.format(res))
    return res
