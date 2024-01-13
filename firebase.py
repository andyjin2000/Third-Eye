import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Initialize Firebase
cred = credentials.Certificate('service_accnt_creds.json')
firebase_admin.initialize_app(cred)

# Access Firestore
db = firestore.client()

# Read data
doc_ref = db.collection('garbage').document('garbage')
try:
    doc = doc_ref.get()
    if doc.exists:
        print('Document data:', doc.to_dict())
    else:
        print('No such document!')
except Exception as e:
    print('Error reading document:', e)