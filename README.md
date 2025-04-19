readme: |
  #  Market Data ETL Pipeline with Airflow (Astro CLI)

  This project is a simple **ETL (Extract, Transform, Load)** pipeline built with **Apache Airflow** using **Astro CLI**. It fetches daily market data for a stock (Amazon - AMZN) from the [Polygon API](https://polygon.io/), transforms the data using pandas, and loads it into a local **SQLite** database.

  ---

  ##  Tech Stack

  - [Astro CLI](https://docs.astronomer.io/astro/cli/overview)
  - Apache Airflow
  - SQLite (mounted `.db` file)
  - Python (Airflow tasks using decorators)
  - Polygon API

  ---

  ##  Project Structure
. ├── dags/ │ └── market_etl.py # Main DAG script ├── include/ ├── plugins/ ├── tests/ ├── airflow_settings.yaml ├── Dockerfile ├── requirements.txt ├── .env # (Optional) Store API keys here ├── sqlite_database/ │ └── market_database.db # Local SQLite DB (mounted into container) └── docker-compose.override.yml
