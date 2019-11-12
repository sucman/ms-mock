import decimal
import json
import datetime


def serialize(model):
    from sqlalchemy.orm import class_mapper
    columns = [c.key for c in class_mapper(model.__class__).columns]
    print(columns)
    return dict((c, getattr(model, c)) for c in columns)


def convert_time(time):
    dt = datetime.datetime.fromtimestamp(time)
    return dt


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        super(DecimalEncoder, self).default(o)
