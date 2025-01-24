import enum
from datetime import datetime

from app.extensions import database


class StatusEnum(str, enum.Enum):
    in_progress = "in_progress"
    sent = "sent"
    paid = "paid"


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
    status = database.Column(
        database.Enum(StatusEnum, native_enum=False, length=36),
        default=StatusEnum.in_progress,
        server_default=StatusEnum.in_progress.value,
        nullable=False,
        index=True,
    )
    time_created = database.Column(
        database.DateTime, nullable=False, default=datetime.now
    )
    time_updated = database.Column(
        database.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )
    user = database.relationship("User", back_populates="claims")
    services = database.relationship("Service")

    def __repr__(self) -> str:
        return "<CLaim: {}>".format(self.services)


class Service(database.Model):  # type: ignore[name-defined,misc]
    __tablename__ = "service"

    id = database.Column(database.Integer, autoincrement=True, primary_key=True)
    claim_id = database.Column(database.Integer, database.ForeignKey("claims.id"))
    service_date = database.Column(
        database.DateTime, nullable=False, default=datetime.now
    )
    service_name = database.Column(database.String(100), nullable=False)
    type = database.Column(database.String(50), nullable=False)
    provider_name = database.Column(database.String(100), nullable=False)
    source = database.Column(database.String(100), nullable=False)
    cost_of_service = database.Column(database.Integer)

    def __repr__(self) -> str:
        return "<Service: {}>".format(self.type)
