class Datos(object):
    """docstring for Datos"""
    direccion = ['319 East Coma Ave',
                 'Suite 689',
                 'Hidalgo Texas USA',
                 'Tel.- +52 (844) 4 12 88 68; (844) 4 10 36 06',
                 'ventas@borbollametrology.com',
                 'www.borbollametrology.com',
                 ]

    datos_cliente = ['Cotizacion : 854698' ,
                 'Cliente       : GOBAR',
                 'Contacto    : Juan Castellanos',
                 'E-mail        : juan.castellanos@gobarsystems.com'
                     ]             
    
    encabezado = ['Cantidad',
                  'Descripcion',
                  'Total']
    cotizacion_rows = [150,300,500]

    logo = 'static/assets/images/borbolla_metrology_logo.jpg'

    texto1 = ['AMPARA HASTA (36 Horas de Labor) disponible lunes-viernes',
              'Horarios 07 am - 3:00 pm sujeto a cambios de a cuerdo a decision del Tecnico de Servicio.',
              'Esta cotizacion tiene validez de 30 DIaws. El costo es en Dolares',
              'Terminos de pago : 30 DIas desde la fecha de facturacion']

    texto2 = ['Para la calibracion espacial y repetitibilidad, se seguira el procedimiento BMI-10360-2 el cual',
              'se basa en la norma ISO-10360-2 secc 6.3.3 agregar la seccion 6.5 se hara por requerimiento',
              'especifico del cliente y que la cotizacion asi lo indique. Para MPE se sequira ']          


    
    def __init__(self, cotizacion = False , Orden = False , Factura = False):
        pass
        
        
