from datetime import datetime

from app.extensions import database


class User(database.Model):  # type: ignore[name-defined,misc]
    __tablename__ = "user"

    id = database.Column(database.Integer, autoincrement=True, primary_key=True)
    name = database.Column(database.String(100), nullable=False, unique=True)
    salary = database.Column(database.Integer, nullable=False)
    gender = database.Column(database.String(10), nullable=True)
    date_of_birth = database.Column(database.Date, nullable=True)
    time_created = database.Column(
        database.DateTime, nullable=False, default=datetime.utcnow
    )
    claim = database.relationship("Claim")

    def __repr__(self) -> str:
        return "<User: {}>".format(self.name)
