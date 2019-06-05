# Data Stack

## 1. Presentation

A sample data stack running on Docker, that contains the following components:

- [Airflow](https://airflow.apache.org/)
- [Metabase](https://metabase.com/)
- [MariaDB](https://mariadb.org/)
- A template python package, usable in Airflow DAGS
- Unit-testing with [unittest](https://docs.python.org/3/library/unittest.html) library
- [Sphinx](http://www.sphinx-doc.org/en/master/) auto-generated documentation

## 2. Installation

You will need to have the following software installed:

- [python3](https://www.python.org/)
- [virtualenv](https://virtualenv.pypa.io/en/latest/)
- [Docker](https://www.docker.com/)
- [docker-compose](https://docs.docker.com/compose/)

Once you're good, create a virtual environment in install the pre-requisite python libraries:

```text
virtualenv venv;
source venv/bin/activate;
pip install -r requirements.txt;
```

## 3. Usage

### 3.1 Launch the Docker stack

Run it with:

``` text
docker-compose up -d
```

Then visit:

- [localhost:3000](http://localhost:3000): for Metabase
- [localhost:8080](http://localhost:8080): for Airflow

Add your Airflow DAGS in the [dags](./dags) folder.

### 3.2 Unit testing

Run the unit tests with:

```text
python -m unittest discover -s tests;
```

### 3.3 Generating the Sphinx docs

Generate the Sphinx documentation with:

```text
sphinx-apidoc ./python_package -o docs/source -M;
cd docs && make html && open build/html/index.html;
```

## 4. References

- [puckel/docker-airflow](https://github.com/puckel/docker-airflow)
