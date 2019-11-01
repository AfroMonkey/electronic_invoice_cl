from lxml import etree

import logging

_logger = logging.getLogger(__name__)


def insert(parent, child, text=""):
    child = etree.Element(child)
    child.text = text
    parent.append(child)


def _process_data(DTE, data):
    insert(DTE, 'Tipo', data['Tipo'])
    insert(DTE, 'Folio', data['Folio'])
    insert(DTE, 'FechaEmision', data['FechaEmision'])
    insert(DTE, 'FechaVencimiento', data['FechaVencimiento'])
    # TODO insert(DTE, 'TipoDespacho', data['TipoDespacho'])
    # TODO insert(DTE, 'TipoTraslado', data['TipoTraslado'])
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
    # TODO insert(DTE, 'TransPatente', data['TransPatente'])
    # TODO insert(DTE, 'TransRutChofer', data['TransRutChofer'])
    # TODO insert(DTE, 'TransNombreChofer', data['TransNombreChofer'])
    # TODO insert(DTE, 'TransDireccionDestino', data['TransDireccionDestino'])
    # TODO insert(DTE, 'TransComunaDestino', data['TransComunaDestino'])
    # TODO insert(DTE, 'TransCiudadDestino', data['TransCiudadDestino'])
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

    _logger.info(etree.tostring(DTE, pretty_print=True))


# data_demo = {
#     'Tipo': '33',
#     'Folio': '16',
#     'FechaEmision': '17-09-2019',
#     'FechaVencimiento': '17-09-2019',
#     'TipoDespacho': '',
#     'TipoTraslado': '',
#     'FormaPago': '2',
#     'GlosaPago': 'Cheque a Fecha',
#     'Sucursal': 'Osorno',
#     'Vendedor': 'Daniel Soto',
#     'ReceptorRut': '96719960-5',
#     'ReceptorRazon': 'AGRICOLA Y COMERCIAL GM LTDA.',
#     'ReceptorGiro': 'EXPLOTACION AGRO-COMERCIAL',
#     'ReceptorContacto': '',
#     'ReceptorDireccion': 'FRANCISCO BILBAO 1860 3er PISO',
#     'ReceptorComuna': 'OSORNO',
#     'ReceptorCiudad': 'OSORNO',
#     'ReceptorFono': '64-235879',
#     'TransPatente': 'DF-5678',
#     'TransRutChofer': '13822280-2',
#     'TransNombreChofer': 'Pedro Sandoval',
#     'TransDireccionDestino': 'FDO EDUVIGES',
#     'TransComunaDestino': 'FUTRONO',
#     'TransCiudadDestino': 'FUTRONO',
#     'Unitarios': '1',
#     'Neto': '22293',
#     'Exento': '',
#     'Iva': '4236',
#     'Total': '30486',
# }

# get_xml(data_demo)
