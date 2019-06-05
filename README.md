# Data Stack

A sample data stack running on Docker, that contains the following services:

- [Airflow](https://airflow.apache.org/) (with its Postgres database)
- [Metabase](https://metabase.com/) (with its Postgres database)
- [MariaDB](https://mariadb.org/) (as main database)

Run it with:

``` text
docker-compose up -d
```

Then visit:

- [localhost:3000](http://localhost:3000): for Metabase
- [localhost:8080](http://localhost:8080): for Airflow

Add your Airflow DAGS in the [airflow-dags](./airflow-dags) folder.

Credits to:

- [puckel/docker-airflow](https://github.com/puckel/docker-airflow)
