SELECT
model.id,
model_name,
optimizer_name,
last_updated,
max(eval_F1) max_F1_score,
count(1) as n_epochs,
(JulianDay(max(epoch.created_at)) - JulianDay(min(epoch.created_at))) * 24 * 60 AS training_minutes
FROM model
JOIN epoch on model.id = epoch.model_id
GROUP BY 1, 2
ORDER BY 5 DESC
