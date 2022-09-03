from apps import db
from sqlalchemy.dialects.mysql import LONGTEXT
from datetime import datetime
from sqlalchemy import event
from flask_login import current_user


def convert_2_long_text(row):
    return ','.join(row)


class Analyzes(db.Model):
    __tablename__ = 'analyzes'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(64))
    aspects = db.Column(LONGTEXT)
    polarities = db.Column(LONGTEXT)
    preprocessed_text = db.Column(LONGTEXT)
    f1score = db.Column(db.Float(5, 2))
    reviewCount = db.Column(db.Integer)
    createdTime = db.Column(db.DateTime, default=datetime.now())
    userId = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, columns):
        # columns['createdTime'] = datetime.now()

        for property, value in columns.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                if type(value[0]) is str:
                    value = convert_2_long_text(value)
                else:
                    # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                    value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return str(self.filename)
