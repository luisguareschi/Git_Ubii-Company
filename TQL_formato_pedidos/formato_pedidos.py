import sqlalchemy
from sqlalchemy import text
from columnar import columnar
import os
### email modules ###
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib, ssl



class Cabecera:
    def __init__(self, tipo_registro, n_documento, n_cliente, desti_mercancia, fecha_entrega, moneda, condicion_pago):
        self.tipo_registro = tipo_registro
        self.tipo_registro = str(self.tipo_registro)
        self.tipo_registro = self.tipo_registro.zfill(2)

        self.n_documento = n_documento
        self.n_documento = str(self.n_documento)
        self.n_documento = self.n_documento.zfill(8)

        self.n_cliente = n_cliente
        self.desti_mercancia = desti_mercancia
        self.fecha_entrega = fecha_entrega
        self.moneda = moneda
        self.condicion_pago = condicion_pago

    def __repr__(self):
        return str(self.tipo_registro) + '\t' + str(self.n_documento) + '\t' + str(self.n_cliente) + '\t' + str(
            self.desti_mercancia) + '\t' + str(self.fecha_entrega) + '\t' + str(self.moneda) + '\t' + str(
            self.condicion_pago) + '\n'

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

class Posicion:
    def __init__(self, tipo_registro, n_documento, material, unidad_medida, cantidad, desti_mercancia=''):
        self.tipo_registro = tipo_registro
        self.tipo_registro = str(self.tipo_registro)
        self.tipo_registro = self.tipo_registro.zfill(2)

        self.n_documento = n_documento
        self.n_documento = str(self.n_documento)
        self.n_documento = self.n_documento.zfill(8)

        self.material = material
        self.unidad_medida = unidad_medida
        self.cantidad = cantidad
        self.desti_mercancia = desti_mercancia

    def __repr__(self):
        if len(str(self.cantidad)) >= 8:
            return str(self.tipo_registro) + '\t' + str(self.n_documento) + '\t' + str(self.material) + '\t' + str(
                self.unidad_medida) + '\t' + str(self.cantidad) + '\t' + str(self.desti_mercancia) + '\n'
        else:
            return str(self.tipo_registro) + '\t' + str(self.n_documento) + '\t' + str(self.material) + '\t' + str(
                self.unidad_medida) + '\t' + str(self.cantidad) + '\t' + '\t' + str(self.desti_mercancia) + '\n'

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

def add(elementos):
    # Ordenar la lista con los datos
    elementos.sort(key=lambda x: x.tipo_registro, reverse=False)
    file = open('formato_txt_pedidos.txt', 'a')
    cabeceros =[]
    posiciones = []
    for elemento in elementos:
        if type(elemento).__name__ == 'Cabecera':
            cabeceros.append(elemento)
        elif type(elemento).__name__ == 'Posicion':
            posiciones.append(elemento)
    cabeceros.sort(key=lambda x: x.n_documento, reverse=False)
    posiciones.sort(key=lambda x: x.n_documento, reverse=False)
    elementos_ordenados = []
    numeros_documentos = []
    cabeceros_ord = []
    posiciones_ord = []
    for item in cabeceros:
        elementos_ordenados.append(item)
        cabeceros_ord.append(item)
        numeros_documentos.append(item.n_documento)
    for item in posiciones:
        if item.n_documento in numeros_documentos:
            elementos_ordenados.append(item)
            posiciones_ord.append(item)
        else:
            print('La posicion con el numero de documento:', item.n_documento, 'no se encuentra en los cabeceros')

    # agregar elementos al archivo txt
    data = []
    for entry in cabeceros_ord:
        d = [entry.tipo_registro, entry.n_documento, entry.n_cliente, entry.desti_mercancia, entry.fecha_entrega, entry.moneda, entry.condicion_pago]
        data.append(d)
        if entry.tipo_registro == '01':
            print('Cabecero con el numero_documento:', entry.n_documento, 'agregado')
    for entry in posiciones_ord:
        d = [entry.tipo_registro, entry.n_documento, entry.material, entry.unidad_medida, entry.cantidad, entry.desti_mercancia, '']
        data.append(d)
        if entry.tipo_registro == '02':
            print('Posicion con el numero_documento:', entry.n_documento, 'agregada')
    tabla = columnar(data, no_borders=False, terminal_width=1000000, column_sep='\t', row_sep='')
    file.write(str(tabla))
    file.close()

    file = open('formato_txt_pedidos.txt')
    final_file = open('data_final.txt', 'a')
    line_number = 1
    for line in file.readlines():
        if line_number % 2 == 0:
            line = line.replace('\t', '', 1)
            final_file.write(line)
        line_number += 1
    file.close()
    final_file.close()
    os.remove('formato_txt_pedidos.txt')
    os.rename('data_final.txt', 'formato_txt_pedidos.txt')
    print('PROCESO EXITOSO, ARCHIVO: formato_txt_pedidos.txt CREADO')

def create_items(results):
    items = []
    for i in results:
        n_documento = i['id_pedido']
        unidad = i['unidad']
        cantidad = i['cantidad']
        fecha = str(i['CreatedOn'])  # VALOR DE PRUEBA
        year = fecha[0] + fecha[1] + fecha[2] + fecha[3]
        month = fecha[5] + fecha[6]
        day = fecha[8] + fecha[9]
        fecha_new = '{}/{}/{}'.format(day, month, year)
        material = i['id_producto']  # VALOR DE PRUEBA
        moneda = 'USD'  # VALOR DE PRUEBA
        condicion_pago = 'PL01'  # VALOR DE PRUEBA
        desti_mercancia = 934264  # VALOR DE PRUEBA
        n_cliente = 124378  # VALOR DE PRUEBA

        cabecero = Cabecera(1, n_documento, n_cliente, desti_mercancia, fecha_new, moneda, condicion_pago)
        posicion = Posicion(2, n_documento, material, unidad, cantidad, desti_mercancia)
        if cabecero not in items:
            items.append(cabecero)
        if posicion not in items and cantidad > 0:
            items.append(posicion)
    return items  # Lista llena de objetos cabecero y posicion

def update_database():
    update_query = text('UPDATE ubiimarket_db.dt_pedido as a, ubiimarket_db.dt_detalle_pedido as b, ubiimarket_db.dt_productos as c, ubiimarket_db.tm_unidad_presentacion as d, ubiimarket_db.dt_lote as e, ubiimarket_db.dt_almacen_ubii as f '
                        'SET a.tb_status_id=37 '
                        'WHERE a.tb_status_id=24 AND a.id=b.dt_pedido_id AND b.id_producto=c.id_producto '
                        'AND c.id_unidad_presentacion=d.id_presentacion AND b.id_lote=e.id_lote '
                        'AND  e.id_almacen_ubii=f.id_almacen AND f.rif=\'J-075525973\'')
    db.engine.execute(update_query)
    print('El estado de los pedido(s)  ha sido cambiado de 24 a 37 exitosamente')

def send_email(receiver, subject, body, file_name):
    fromaddr = 'no-reply@ubiimarket.com'
    toaddrs = receiver
    username = 'no-reply@ubiimarket.com'
    password = 'ubiimarket.2020'

    msg = MIMEMultipart()
    msg["From"] = fromaddr
    msg['To'] = toaddrs
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # file_name = 'datos_para_destinatario_mercancia.txt'
    file = open(file_name, 'rb')
    part = MIMEBase("application", "octet-stream")
    part.set_payload(file.read())
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {file_name}",
    )
    msg.attach(part)
    text = msg.as_string()

    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL('correo.ubiimarket.com', 465, context=context)
    server.login(username, password)
    server.sendmail(fromaddr, toaddrs, text)
    server.quit()
    print('El correo ha sido enviado exitosamente')

    #### CAMBIARLO A SSL #####

# Acceder a la base de datos
username = 'lguareschi'
password = 'L01SGSc1r*20'
ip = '172.16.24.35'
port = '3306'
db_name = 'ubiimarket_db'
db = sqlalchemy.create_engine('mysql+pymysql://{}:{}@{}:{}/{}'.format(username, password, ip, port, db_name), pool_recycle=3600)

# Crear los archivos txt
file = open('formato_txt_pedidos.txt', 'w')
file.close()
file2 = open('data_final.txt', 'w')
file2.close()

# Hacer Query de los datos necesarios
query = text('SELECT a.id as id_pedido, a.tb_status_id, b.id_producto, c.id_unidad_presentacion, d.strsiglas as unidad, b.intcantidad as cantidad, b.id_lote, e.id_almacen_ubii, f.nombre_almacen, b.CreatedOn '
             'FROM ubiimarket_db.dt_pedido as a, ubiimarket_db.dt_detalle_pedido as b, ubiimarket_db.dt_productos as c, '
             'ubiimarket_db.tm_unidad_presentacion as d, ubiimarket_db.dt_lote as e, ubiimarket_db.dt_almacen_ubii as f '
             'WHERE a.tb_status_id=24 AND a.id=b.dt_pedido_id AND b.id_producto=c.id_producto AND c.id_unidad_presentacion=d.id_presentacion '
             'AND b.id_lote=e.id_lote AND e.id_almacen_ubii=f.id_almacen AND f.rif=\'J-075525973\'')
results = db.engine.execute(query).fetchall()

# Crear lista de datos para agregar al txt
items = create_items(results)

# Agregar lista de datos al txt
add(items)

# Enviar correo electronico con el archivo txt
receiver = 'pvalencia@ubiipagos.com'
subject = 'formato_pedidos'
body = ''
file_name = 'formato_txt_pedidos.txt'
# send_email(receiver, subject, body, file_name)

# actualizar base de datos (cambiar estado de pedido de 24-->37)
# update_database()

'''NOTA DE QUE FALTA POR HACER:
--------------------------------
1-) CAMBIAR LOS DATOS DE PRUEBA POR DATOS VERDADEROS
2-) ESPERAR INSTRUCCIONES DE PATRICIA
'''
