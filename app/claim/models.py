from datetime import datetime

from app.extensions import database


class Claim(database.Model):  # type: ignore[name-defined,misc]
    __tablename__ = "claims"

    id = database.Column(database.Integer, autoincrement=True, primary_key=True)
    user_id = database.Column(database.Integer, database.ForeignKey("user.id"))
    diagnosis = database.Column(database.String(1000))
    hmo = database.Column(database.String(4))
    age = database.Column(database.Integer, nullable=True)
    service_charge = database.Column(database.Integer)
    total_cost = database.Column(database.Integer)
    final_cost = database.Column(database.Integer)
    user = database.relationship("User", back_populates="claims")
    service = database.relationship("Service")

    def __repr__(self) -> str:
        return "<CLaim: {}>".format(self.service)


class Service(database.Model):  # type: ignore[name-defined,misc]
    __tablename__ = "service"

    id = database.Column(database.Integer, autoincrement=True, primary_key=True)
    claim_id = database.Column(database.Integer, database.ForeignKey("claims.id"))
    service_date = database.Column(
        database.DateTime, nullable=False, default=datetime.utcnow
    )
    service_name = database.Column(database.String(100), nullable=False, unique=True)
    type = database.Column(database.String(50), nullable=False, unique=True)
    provider_name = database.Column(database.String(100), nullable=False, unique=True)
    source = database.Column(database.String(100), nullable=False, unique=True)
    cost_of_service = database.Column(database.Integer)

    def __repr__(self) -> str:
        return "<Service: {}>".format(self.type)
