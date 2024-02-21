from app.backend.db.models import ContactModel
from datetime import datetime
from sqlalchemy import func



class Contactclass:
    def __init__(self, db):
        self.db = db

    def update_contact(self, data):
        contact = self.db.query(ContactModel).first()
        contact.text = data.text
        contact.updated_date = datetime.now()

        self.db.commit()

        return 1
    
    def get_contact(self):
        contact = self.db.query(ContactModel).first()
        return contact