# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from email.policy import default
from apps import db
from sqlalchemy.exc import SQLAlchemyError
from apps.exceptions.exception import InvalidUsage
import datetime as dt
from sqlalchemy.orm import relationship
from enum import Enum

class CURRENCY_TYPE(Enum):
    usd = 'usd'
    eur = 'eur'

class Product(db.Model):

    __tablename__ = 'products'

    id            = db.Column(db.Integer,      primary_key=True)
    name          = db.Column(db.String(128),  nullable=False)
    info          = db.Column(db.Text,         nullable=True)
    price         = db.Column(db.Integer,      nullable=False)
    currency      = db.Column(db.Enum(CURRENCY_TYPE), default=CURRENCY_TYPE.usd, nullable=False)

    date_created  = db.Column(db.DateTime,     default=dt.datetime.utcnow())
    date_modified = db.Column(db.DateTime,     default=db.func.current_timestamp(),
                                               onupdate=db.func.current_timestamp())
    
    def __init__(self, **kwargs):
        super(Product, self).__init__(**kwargs)

    def __repr__(self):
        return f"{self.name} / ${self.price}"

    @classmethod
    def find_by_id(cls, _id: int) -> "Product":
        return cls.query.filter_by(id=_id).first() 

    def save(self) -> None:
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)

    def delete(self) -> None:
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)
        return


#__MODELS__
class User(db.Model):

    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)

    #__User_FIELDS__
    id_user = db.Column(db.Integer, nullable=True)
    created_by = db.Column(db.String(255),  nullable=True)
    created_date = db.Column(db.Integer, nullable=True)
    last_modify_by = db.Column(db.String(255),  nullable=True)
    last_modify_date = db.Column(db.Integer, nullable=True)
    username = db.Column(db.String(255),  nullable=True)
    email = db.Column(db.String(255),  nullable=True)
    password = db.Column(db.String(255),  nullable=True)
    role = db.Column(db.String(255),  nullable=True)
    status = db.Column(db.Integer, nullable=True)

    #__User_FIELDS__END

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)


class Integrations(db.Model):

    __tablename__ = 'Integrations'

    id = db.Column(db.Integer, primary_key=True)

    #__Integrations_FIELDS__
    id_integration = db.Column(db.Integer, nullable=True)
    name = db.Column(db.String(255),  nullable=True)
    description = db.Column(db.Text, nullable=True)
    target_url = db.Column(db.String(255),  nullable=True)
    auth_type = db.Column(db.String(255),  nullable=True)
    cred_key = db.Column(db.String(255),  nullable=True)
    cert_path = db.Column(db.String(255),  nullable=True)
    method = db.Column(db.String(255),  nullable=True)
    content_type = db.Column(db.String(255),  nullable=True)
    execution_mode = db.Column(db.String(255),  nullable=True)
    retry_count = db.Column(db.String(255),  nullable=True)
    timeout_sec = db.Column(db.String(255),  nullable=True)
    active = db.Column(db.String(255),  nullable=True)

    #__Integrations_FIELDS__END

    def __init__(self, **kwargs):
        super(Integrations, self).__init__(**kwargs)



#__MODELS__END
