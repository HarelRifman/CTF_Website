import os, json
import firebase_admin
from firebase_admin import credentials, db

cred_env = os.environ.get("FIREBASE_CREDENTIALS_JSON")
db_url = os.environ.get("FIREBASE_DB_URL")

if cred_env:
    cred_dict = json.loads(cred_env)
    cred = credentials.Certificate(cred_dict)
else:
    cred = credentials.Certificate("firebase-credentials.json")

firebase_admin.initialize_app(cred, {
    "databaseURL": db_url or "https://your-project-id.firebaseio.com"
})

# Firebase Handler Class
class FirebaseHandler:
    def __init__(self, reference_name):
        self.db_ref = db.reference(reference_name)

    def add_record(self, record_id, details):
        try:
            self.db_ref.child(record_id).set(details)
            return True
        except Exception as error:
            print(f"Firebase error: {error}")
            return False

    def get_record(self, record_id):
        try:
            record = self.db_ref.child(record_id).get()
            return record
        except Exception as error:
            print(f"Firebase error: {error}")
            return None

    def update_record(self, record_id, updates):
        try:
            self.db_ref.child(record_id).update(updates)
            return True
        except Exception as error:
            print(f"Firebase error: {error}")
            return False

    def get_all_records(self):
        try:
            records = self.db_ref.get()
            return records or {}
        except Exception as error:
            print(f"Firebase error: {error}")
            return {}
