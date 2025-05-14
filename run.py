from firebase_admin import db
import firebase_admin
from firebasePhandler import CREDENTIALS_PATH

# Firebase Setup
credentials = firebase_admin.credentials.Certificate(CREDENTIALS_PATH)
firebase_admin.initialize_app(credentials, {
    'databaseURL': "https://ex2db-5c4eb-default-rtdb.firebaseio.com/"
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
