# Data Stack

## Presentation

A sample data stack running on Docker, that contains the following services:

- [Airflow](https://airflow.apache.org/)
- [Metabase](https://metabase.com/)
- [MariaDB](https://mariadb.org/)

There is also a python package containing an example module, used by the
example Airflow DAG.

## Usage

Run it with:

``` text
docker-compose up -d
```

Then visit:

- [localhost:3000](http://localhost:3000): for Metabase
- [localhost:8080](http://localhost:8080): for Airflow

Add your Airflow DAGS in the [dags](./dags) folder.

## References

- [puckel/docker-airflow](https://github.com/puckel/docker-airflow)
