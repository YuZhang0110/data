# Prepare

```sudo apt-get remove docker docker-engine docker.io containerd runc```
```apt install postgresql-client```
```pip install awscli-local```

# To ruun
type this in your terminal

```
git clone git@github.com:YuZhang0110/data-engineer-fetch.git
cd data-engineering-fetch-rewards
```

Run make command to install dependencies.

```make pip-install```

Run make command to configure aws shell.

```make aws-configure```

Pull and start docker containers.

```make start```

Run Python code to perform ETL process

```make perform-etl```

# Checking messages loaded in Postgres

To validate the messages loaded in Postgres

```psql -d postgres -U postgres -p 5432 -h localhost -W```

Credentials and database information

    * username=postgres
    * password=postgres
    * database=postgres
