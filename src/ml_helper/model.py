import uuid
from datetime import datetime

import sqlalchemy as db
from sqlalchemy_utils import UUIDType
from sqlalchemy.orm import relationship

from .db import Base


class Model(Base):
    __tablename__ = "model"
    __table_args__ = (
        db.UniqueConstraint(
            "id", "model_name", "optimizer_name", name="unique_model"
        ),
    )

    uuid = db.Column(UUIDType, primary_key=True, default=uuid.uuid4)

    id = db.Column(db.String)
    last_updated = db.Column(db.DateTime,
                             default=datetime.now,
                             onupdate=datetime.now)
    model_name = db.Column(db.String)
    model_params = db.Column(db.JSON)

    optimizer_name = db.Column(db.String)
    optimizer_params = db.Column(db.JSON)

    epoch = relationship("Epoch", cascade="all, delete", passive_deletes=True)


class Epoch(Base):
    __tablename__ = "epoch"
    __table_args__ = (
        db.UniqueConstraint("model_id", "number", name="unique_epoch"),
    )

    uuid = db.Column(UUIDType, primary_key=True, default=uuid.uuid4)
    model_id = db.Column(
        db.String,
        db.ForeignKey('model.id', ondelete="cascade"),
    )

    created_at = db.Column(db.DateTime, default=datetime.now)

    number = db.Column(db.Integer)
    training_loss = db.Column(db.Float)
    training_F1 = db.Column(db.Float)
    eval_F1 = db.Column(db.Float)
