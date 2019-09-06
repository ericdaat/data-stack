import hashlib

from sqlalchemy import func

from .db import Session
from .model import Model, Epoch


def _commit_object(obj):
    session = Session()
    session.add(obj)
    session.commit()


def register_model_in_db(model_id, model_params, model_name,
                         optimizer_params, optimizer_name):
    model = Model(
        id=model_id,
        model_name=model_name,
        model_params=model_params,
        optimizer_name=optimizer_name,
        optimizer_params=optimizer_params
    )

    _commit_object(model)


def register_epoch_in_db(model_id, epoch_number,
                         training_loss, training_F1, eval_F1):
    epoch_result = Epoch(
        model_id=model_id,
        number=epoch_number,
        training_loss=training_loss,
        training_F1=training_F1,
        eval_F1=eval_F1
    )

    _commit_object(epoch_result)


def retrieve_best_model_params():
    session = Session()

    result = session.query(Model, func.max(Epoch.eval_F1))\
                    .join(Epoch)\
                    .group_by(Model.id)\
                    .order_by(Epoch.eval_F1.desc())\
                    .first()

    return dict(
        model_name=result[0].model_name,
        model_params=result[0].model_params,
        optimizer_name=result[0].optimizer_name,
        optimizer_params=result[0].optimizer_params,
        best_eval_f1_score=result[-1]
    )


def hash_parameters(model_params, model_name,
                    optimizer_params, optimizer_name):
    string = str(model_params)\
             + str(model_name)\
             + str(optimizer_params)\
             + str(optimizer_name)

    params_hash = hashlib.sha256(str(string).encode()).hexdigest()

    return params_hash


def delete_model(model_id):
    session = Session()
    session.query(Model).filter_by(id=model_id).delete()
    session.query(Epoch).filter_by(model_id=model_id).delete()
    session.commit()
