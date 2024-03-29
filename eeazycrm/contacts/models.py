from datetime import datetime
from eeazycrm import db
from flask import request
from flask_login import current_user


class Contact(db.Model):
    __tablename__ = "contact"
    id = db.Column(db.Integer, db.Sequence('contact_id_seq'), primary_key=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    avatar = db.Column(db.String(25))
    phone = db.Column(db.String(20), nullable=False)
    mobile = db.Column(db.String(20))
    parentnumber = db.Column(db.String(20), nullable=False)
    etablissement = db.Column(db.String(50), nullable=False)
    nb_choix = db.Column(db.String(50), nullable=False)
    classe = db.Column(db.String(20), nullable=False)
    address_line = db.Column(db.String(40))
    addr_state = db.Column(db.String(40))
    addr_city = db.Column(db.String(40))
    post_code = db.Column(db.String(20))
    country = db.Column(db.String(40))
    notes = db.Column(db.String(200))
    stage = db.Column(db.String(100), default ="Nouveau")
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'), nullable=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id', ondelete='cascade'), nullable=False)

    @staticmethod
    def contact_list_query():
        account = request.args.get('acc', None, type=int)
        if current_user.is_admin:
            contacts = Contact.query\
                .filter(Contact.account_id == account if account else True)
        else:
            contacts = Contact.query \
                .filter(Contact.account_id == account if account else True) \
                .filter(Contact.owner_id == current_user.id)
        return contacts

    @staticmethod
    def get_label(contact):
        return contact.first_name + ' ' + contact.last_name

    @staticmethod
    def get_contact(contact_id):
        return Contact.query.filter_by(id=contact_id).first()

    def get_contact_name(self):
        if self.last_name:
            return self.first_name + ' ' + self.last_name
        else:
            return None

    def __repr__(self):
        return f"Account('{self.last_name}', '{self.email}', '{self.phone}')"
