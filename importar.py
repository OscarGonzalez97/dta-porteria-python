import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import openpyxl
from datetime import datetime, timedelta

wookbook = openpyxl.load_workbook("ReportePorteria.xlsx")
# Define variable to read the active sheet:
worksheet = wookbook.active

# Use a service account.
# quitar credenciales en firebase console -> proyecto -> configuracion de proyecto -> cuentas de servicio -> SDK Firebase admin -> Generar nueva clave privada
cred = credentials.Certificate('porteria-dta-firebase-adminsdk-hml1j-55255f2fb1.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()

# Archivo columnas ID-SOCIO-APELLIDO_NOMBRE-EDAD-NRO_CI-CATEGORIA-MES CUOTA
for i in range(7, worksheet.max_row):
    # CI persona
    if worksheet[f'G{i}'].value:
        cedula = worksheet[f'G{i}'].value
    else:
        cedula = worksheet[f'C{i}'].value
    # al dia o no
    if worksheet[f'I{i}'].value:
        fecha_al_dia = datetime.now() - timedelta(days=60)
        al_dia = str(datetime.strptime(worksheet[f'H{i}'].value, '%d/%m/%Y') < fecha_al_dia).lower()
    else:
        al_dia = 'false'
    # nombre y apellido
    nombre = worksheet[f'E{i}'].value
    apellido = worksheet[f'D{i}'].value
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
