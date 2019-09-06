SELECT
model.model_name,
model.last_updated,
model.model_params,
model.optimizer_name,
model.optimizer_params
FROM model
WHERE model.id = {{id}}
