from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from .models import LocalAuthority, Hours, TravelMethod, TravelDistance, User, Map
from .extensions import db


class LocalAuthoritySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = LocalAuthority
        load_instance = True


class HoursSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Hours
        load_instance = True


class TravelMethodSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TravelMethod
        load_instance = True


class TravelDistanceSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TravelDistance
        load_instance = True


class MapSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Map
        load_instance = True


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ['password_hash']
        sqla_session = db.session
        include_relationships = True
