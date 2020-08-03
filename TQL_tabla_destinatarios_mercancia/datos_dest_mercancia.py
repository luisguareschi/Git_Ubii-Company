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


class Datos_destinatario:
    def __init__(self, nombre, direccion, codigo_postal, tlfn, rif, zona_transporte, persona_contacto,
                 centro_suministrador):
        self.nombre = nombre
        self.direccion = direccion
        self.codigo_postal = codigo_postal
        self.tlfn = tlfn
        self.rif = rif
        self.zona_transporte = zona_transporte
        self.persona_contacto = persona_contacto
        self.centro_suministrador = centro_suministrador

    def __repr__(self):
        return str(self.nombre) + '\t' + str(self.direccion) + '\t' + str(self.codigo_postal) + '\t' + str(
            self.tlfn) + '\t' + str(self.rif) + '\t' + str(self.zona_transporte) + '\t' + str(
            self.persona_contacto) + '\t' + str(self.centro_suministrador) + '\n'

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


def add(results, results2):
    # Agregar datos
    file = open('datos.txt', 'a')
    header = ['NOMBRE', 'DIRECCION', 'CODIGO POSTAL', 'TELEFONO', 'RIF', 'ZONA DE TRANSPORTE', 'PERSONA DE CONTACTO',
              'CENTRO SUMINISTRADOR']
    todos_datos = []
    todos_datos.append(header)
    for item in results:  # id_political_div = Null
        nombre = item['strnombre_empresa']
        direccion = str(item['zona']) + ', ' + str(item['subzona']) + ', ' + str(item['strdireccion'])
        codigo_postal = item['strcodigo_postal']
        tlfn = item['strtelefono']
        rif = item['strrif_empresa']
        zona_transporte = '<ZONA DEFINIDA POR TQL>'  # FALTA DATO! QUEDA POR DEFINIR POR PARTE DE TQL
        persona_contacto = ''  # PUEDE SER BLANCO
        centro_suministrador = ''  # POR AHORA VACIO
        datos = Datos_destinatario(nombre, direccion, codigo_postal, tlfn, rif, zona_transporte, persona_contacto,
                                   centro_suministrador)
        d = [datos.nombre, datos.direccion, datos.codigo_postal, datos.tlfn, datos.rif, datos.zona_transporte,
             datos.persona_contacto, datos.centro_suministrador]
        todos_datos.append(d)
        print('Entrada agregada exitosamente')

    for item in results2:  # id_political_div != Null
        nombre = item['strnombre_empresa']
        ######## PARA DIRECCION ########
        estado = item['state'].lower()
        estado = estado.capitalize()
        ciudad = item['city'].lower()
        ciudad = ciudad.capitalize()
        municipalidad = item['municipality'].lower()
        municipalidad = municipalidad.capitalize()
        parroquia = item['parish'].lower()
        parroquia = parroquia.capitalize()
        direccion = estado + ', ' + ciudad + ', ' + municipalidad + ', ' + parroquia + ', ' + str(item['strdireccion'])
        ################################
        codigo_postal = item['strcodigo_postal']
        tlfn = item['strtelefono']
        rif = item['strrif_empresa']
        zona_transporte = '<ZONA DEFINIDA POR TQL>'  # FALTA DATO! QUEDA POR DEFINIR POR PARTE DE TQL
        persona_contacto = ''  # PUEDE SER BLANCO
        centro_suministrador = ''  # POR AHORA VACIO
        datos2 = Datos_destinatario(nombre, direccion, codigo_postal, tlfn, rif, zona_transporte, persona_contacto,
                                    centro_suministrador)
        d2 = [datos2.nombre, datos2.direccion, datos2.codigo_postal, datos2.tlfn, datos2.rif, datos2.zona_transporte,
              datos2.persona_contacto, datos2.centro_suministrador]
        todos_datos.append(d2)
        print('Entrada agregada exitosamente')

    tabla = columnar(todos_datos, no_borders=False, terminal_width=1000000, column_sep='\t', row_sep='')
    file.write(str(tabla))
    file.close()

    # Terminar de organizar tabla
    file = open('datos.txt')
    final_file = open('datos_para_destinatario_mercancia.txt', 'a')
    line_number = 1
    for line in file.readlines():
        if line_number % 2 == 0:
            line = line.replace('\t', '', 1)
            final_file.write(line)
        line_number += 1
    file.close()
    final_file.close()
    print('PROCESO EXITOSO, {} ENTRADAS CREADAS'.format(len(todos_datos)))
    os.remove('datos.txt')


def update_database():
    update_query = text('UPDATE ubiimarket_db.dt_empresa as a, ubiimarket_db.dt_direccion as b '
                        'SET b.nueva_tql=0 '
                        'WHERE a.id_empresa=b.id_empresa AND b.tipo=\'Dirección Fiscal\' AND b.nueva_tql=1')
    db.engine.execute(update_query)
    print('Base de datos actualizada exitosamente')


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
db = sqlalchemy.create_engine('mysql+pymysql://{}:{}@{}:{}/{}'.format(username, password, ip, port, db_name),
                              pool_recycle=3600)

# Crear archivo de destinatario de mercancia.txt
file = open('datos.txt', 'w')
file.close()
final_file = open('datos_para_destinatario_mercancia.txt', 'w')
final_file.close()

# Hacer Query de los datos necesarios
query = text(
    'SELECT a.strnombre_empresa, b.strdireccion, a.strcodigo_postal, a.strtelefono, a.strrif_empresa, a.strnombre_representante, b.nueva_tql, b.id_zona, c.zona, b.id_subzona, d.subzona '
    'FROM ubiimarket_db.dt_empresa as a, ubiimarket_db.dt_direccion as b, ubiimarket_db.dt_zona as c, ubiimarket_db.dt_subzonas as d '
    'WHERE a.id_empresa=b.id_empresa AND b.tipo=\'Dirección Fiscal\' AND b.nueva_tql=1 AND b.id_zona=c.id AND b.id_subzona=d.id AND b.id_political_division is null')
results = db.engine.execute(query).fetchall()

query2 = text(
    'SELECT a.strnombre_empresa, b.strdireccion, a.strcodigo_postal, a.strtelefono, a.strrif_empresa, a.strnombre_representante, b.nueva_tql, b.id_zona, c.zona, b.id_subzona, d.subzona, b.id_political_division, e.state, e.city, e.municipality, e.parish '
    'FROM ubiimarket_db.dt_empresa as a, ubiimarket_db.dt_direccion as b, ubiimarket_db.dt_zona as c, ubiimarket_db.dt_subzonas as d, ubiimarket_db.dt_political_division as e '
    'WHERE a.id_empresa=b.id_empresa AND b.tipo=\'Dirección Fiscal\' AND b.nueva_tql=1 AND b.id_zona=c.id AND b.id_subzona=d.id AND b.id_political_division=e.id;')
results2 = db.engine.execute(query2).fetchall()
# Agregar datos al txt
add(results, results2)

# Enviar correo electonico con el archivo txt
receiver = 'pvalencia@ubiipagos.com'
subject = 'datos_para_destinatario_mercancia'
body = ''
file_name = 'datos_para_destinatario_mercancia.txt'
# send_email(receiver, subject, body, file_name)

# Hacer query para actualizar la tabla
# update_database()
