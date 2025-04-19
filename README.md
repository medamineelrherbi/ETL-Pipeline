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
.
├── dags/  
│ └── market_etl.py # Main DAG script  
├── include/  
├── plugins/  
├── tests/  
├── airflow_settings.yaml  
├── Dockerfile  
├── requirements.txt  
├── .env # (Optional) Store API keys here  
├── sqlite_database/  
│ └── market_database.db # Local SQLite DB (mounted into container in the file docker-compose.yml)  
└── docker-compose.override.yml    

---

## Setup Instructions

### 1. Prerequisites

- [Install Astro CLI](https://docs.astronomer.io/astro/cli/install-astro)
- [Docker installed and running](https://docs.docker.com/get-docker/)
- A free [Polygon.io](https://polygon.io/) API key

---

### 2. ✅ Running the Project

```bash
# Clone this project and enter the directory
git clone <your-repo-url>
cd <project-folder>

# Start Airflow via Astro CLI
astro dev start
```
### 3. Mount the SQLite Database
In docker-compose.override.yml, we mount the SQLite file into the container:  
```
services:
  scheduler:
    volumes:
      - ./sqlite_database/market_database.db:/usr/local/airflow/market_database.db
  webserver:
    volumes:
      - ./sqlite_database/market_database.db:/usr/local/airflow/market_database.db
```
## Airflow Connection Setup
Create connection in Airflow UI:
- Conn Id: market_database_conn  
- Conn Type: SQLite  
- Database: /usr/local/airflow/market_database.db  

## 🔁 DAG Overview
| Task                | Description                      |
|---------------------|----------------------------------|
| hit_polygon_api     | Fetches market data              |
| flatten_market_data | Transforms data to DataFrame     |
| load_market_data    | Loads to SQLite database         |

Runs daily starting March 6, 2025.

## 🔍 Verify Data
```sql
SELECT * FROM market_data LIMIT 5;
