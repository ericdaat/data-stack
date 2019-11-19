start-airflow:
	docker-compose up -d airflow-scheduler airflow-flower airflow-worker

docs:
	sphinx-apidoc ./src -o docs/source -M;
	cd docs && make clean && make html && open build/html/index.html;
