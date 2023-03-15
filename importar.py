import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import openpyxl
from datetime import datetime, timedelta

wookbook = openpyxl.load_workbook("REPORTE_PORTERIA_121022.xlsx")
# Define variable to read the active sheet:
worksheet = wookbook.active

# Use a service account.
# quitar credenciales en firebase console -> proyecto -> configuracion de proyecto -> cuentas de servicio -> SDK Firebase admin -> Generar nueva clave privada
cred = credentials.Certificate('porteria-dta-test-firebase-adminsdk-b7ap4-93a77e21af.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()

# Archivo columnas ID-SOCIO-APELLIDO_NOMBRE-EDAD-NRO_CI-CATEGORIA-MES CUOTA
for i in range(7, worksheet.max_row):
    # CI persona
    if worksheet[f'F{i}'].value:
        cedula = worksheet[f'F{i}'].value
    else:
        cedula = worksheet[f'C{i}'].value
    # al dia o no
    if worksheet[f'H{i}'].value:
        fecha_al_dia = datetime.now() - timedelta(days=60)
        al_dia = str(datetime.strptime(worksheet[f'H{i}'].value, '%d/%m/%Y') < fecha_al_dia).lower()
    else:
        al_dia = 'false'
    # nombre y apellido
    nombre_apellido_list = worksheet[f'D{i}'].value.split(' ')
    nombre = f'{nombre_apellido_list[-1]} {nombre_apellido_list[-2]}'
    apellido = ' '.join(nombre_apellido_list[:-2])
    # nro socio
    nro_socio = worksheet[f'C{i}'].value
    doc_ref = db.collection(u'MEMBERS')
    doc_ref.add({
        "created_by": "python_script",
        "id_member": str(nro_socio),
        "is_defaulter": al_dia,
        "name": nombre,
        "surname": apellido,
        "photo": "",
        "type": "Socio",
        "fecha_vencimiento": "",
        "ci": str(cedula)
    })
