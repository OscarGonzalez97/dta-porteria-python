import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account.
# quitar credenciales en firebase console -> proyecto -> configuracion de proyecto -> cuentas de servicio -> SDK Firebase admin -> Generar nueva clave privada
cred = credentials.Certificate('porteria-dta-test-firebase-adminsdk-b7ap4-93a77e21af.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()

# todo: Esto debe hacerse en un ciclo recorriendo el archivo excel
doc_ref = db.collection(u'MEMBERS').document(u'123')
doc_ref.set({
        "created_by": "python_script",
        "id_member": "4333",
        "is_defaulter": "false", # calcular en base a la fecha
        "name": "ACOSTA  F.",
        "surname": "asdf",
        "photo": "",
        "type": "Socio",
})
