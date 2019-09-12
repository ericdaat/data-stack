import hashlib

from sqlalchemy import func

from .model import Session, Model, Epoch


def _commit_object(obj):
    session = Session()
    session.add(obj)
    session.commit()


def register_model_in_db(model_id, params):
    model = Model(
        id=model_id,
        params=params,
    )

    _commit_object(model)


def register_epoch_in_db(model_id, epoch_number, **kwargs):
    epoch_result = Epoch(
        model_id=model_id,
        number=epoch_number,
        **kwargs,
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


def hash_parameters(params):
    params_hash = hashlib.sha256(str(params).encode()).hexdigest()

    return params_hash


def delete_model(model_id):
    session = Session()
    session.query(Model).filter_by(id=model_id).delete()
    session.query(Epoch).filter_by(model_id=model_id).delete()
    session.commit()
