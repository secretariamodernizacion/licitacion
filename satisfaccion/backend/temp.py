from load import *
from base.models import Institucion


Institucion.objects.get_or_create(nombre='SERVICIO NACIONAL DEL PATRIMONIO CULTURAL')


def procesar(nombre, codigo):
    institucion = Institucion.objects.get(nombre=nombre)
    if len(codigo) == 3:
        codigo = '0' + codigo
    if institucion.datos.get("codigo_dipres") != codigo:
        institucion.datos["codigo_dipres"] = codigo

    institucion.save()


procesar('Subsecretaría del Interior', '502')
procesar('Subsecretaría de Relaciones Exteriores', '601')
procesar('Subsecretaría de Economía y Empresas de Menor Tamaño', '701')
procesar('Servicio Nacional del Consumidor', '702')
procesar('Servicio Nacional de Pesca y Acuicultura', '704')
procesar('Instituto Nacional de Estadísticas', '707')
procesar('Dirección de Presupuesto', '802')
procesar('Servicio de Impuestos Internos', '803')
procesar('Servicio Nacional de Aduanas', '804')
procesar('Servicio de Tesorerías', '805')
procesar('Dirección de Compras y Contratación Pública', '807')
procesar('Dirección Nacional del Servicio Civil', '815')
procesar('Superintendencia de Casinos de Juego', '817')
procesar('Comisión para el Mercado Financiero', '831')
procesar('Subsecretaria de Educación', '901')
procesar('Archivo Nacional', '903')
procesar('Junta Nacional de Auxilio Escolar y Becas', '909')
procesar('Junta Nacional de Jardines Infantiles', '911')
procesar('Subsecretaría de Justicia', '1001')
procesar('Servicio de Registro Civil e Identificación', '1002')
procesar('Subsecretaría de Bienes Nacionales', '1401')
procesar('Dirección del Trabajo', '1502')
procesar('Dirección General de Crédito Prendario', '1504')
procesar('Servicio Nacional de Capacitación y Empleo', '1505')
procesar('Superintendencia de Seguridad Social', '1506')
procesar('Superintendencia de Pensiones', '1507')
procesar('ChileAtiende', '1509')
procesar('INSTITUTO DE PREVISION SOCIAL', '1509')
procesar('Instituto de Seguridad Laboral', '1510')
procesar('Caja de Previsión de la Defensa Nacional', '1513')
procesar('Dirección de Previsión de Carabineros de Chile', '1514')
procesar('Fondo Nacional de Salud', '1602')
procesar('Instituto de Salud Pública', '1604')
procesar('Subsecretaría de Salud Pública (COMPIN)', '1609')
procesar('Superintendencia de Salud', '1611')
procesar('Subsecretaría de Vivienda y Urbanismo', '1801')
procesar('SERVIU Región de Tarapacá', '1821')
procesar('SERVIU Región de Antofagasta', '1822')
procesar('SERVIU Región de Atacama', '1823')
procesar('SERVIU Región de Coquimbo', '1824')
procesar('SERVIU Región de Valparaíso', '1825')
procesar('SERVIU Región del Libertador General Bernardo O'Higgins','1826')
procesar('SERVIU Región del Maule', '1827')
procesar('SERVIU Región del Biobío', '1828')
procesar('SERVIU Región de la Araucanía', '1829')
procesar('SERVIU Región de Los Lagos', '1830')
procesar('SERVIU Región de Aysén del Gral. Carlos Ibáñez del Campo', '1831')
procesar('SERVIU Región de Magallanes y  Antartica Chilena', '1832')
procesar('SERVIU Región Metropolitana', '1833')
procesar('SERVIU Región de Los Ríos', '1834')
procesar('SERVIU Región de Arica y Parinacota', '1835')
procesar('SERVIU Región de Ñuble', '1836')
procesar('Subsecretaría de Transportes', '1901')
procesar('Subsecretaría de Servicios Sociales', '2101')
procesar('Fondo de Solidaridad e Inversion Social', '2102')
procesar('Servicio Nacional del Adulto Mayor', '2108')
procesar('Superintendencia de Electricidad y Combustibles', '2404')
procesar('Servicio Nacional del Patrimonio Archivo Nacional', '2903')
procesar('Dirección de Presupuestos', '801')
procesar('Instituto de Desarrollo Agropecuario', '1303')
procesar('Instituto Nacional de Propiedad Industrial', '723')
procesar('Servicio Agrícola y Ganadero', '1304')
procesar('Servicio de Cooperación Técnica', '716')
procesar('Servicio Nacional de Turismo', '709')
procesar('Subsecretaría de Educación', '901')
procesar('Corporación Nacional de Desarrollo Indígena', '2106')
