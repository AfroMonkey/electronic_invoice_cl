from lxml import etree

import logging

_logger = logging.getLogger(__name__)


def insert(parent, child, text=""):
    child = etree.Element(child)
    child.text = text
    parent.append(child)


def get_xml(data):
    DTE = etree.Element('DTE', version='1.0')
    insert(DTE, 'Tipo', data['Tipo'])
    insert(DTE, 'Folio', data['Folio'])
    insert(DTE, 'FechaEmision', data['FechaEmision'])
    insert(DTE, 'FechaVencimiento', data['FechaVencimiento'])
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
