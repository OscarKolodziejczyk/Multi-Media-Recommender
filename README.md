# Overview

This project is a multimedia recommendation engine designed to cross-reference
and suggest movies, books, and video games based on deep semantic
narrative similarities rather than basic genre tags.

By leveraging Language Processing models and a highly optimized vector
database, this system "understands" plot summaries of a requested piece of
media and calculates cosine-similarity to find
thematically similar stories across entertainment mediums.

# The Architecture & Tech Stack

This application is built using a modern, cloud-native engineering pipeline with
strict separation of concerns across data ingestion, machine learning
generation, and API deployment.

Cloud Storage / Data Lake: Azure Blob Storage

Database: PostgreSQL (Containerized via Docker)

Vector Engine: pgvector extension for native SQL math operations

Machine Learning: Hugging Face `all-MiniLM-L6-v2` (Local Execution)

Data Processing Pipeline: Python, Pandas, SQLAlchemy

Backend API: FastAPI (In Progress)

Cloud Deployment: Docker & Azure Container Apps (In Progress)

Unit Testing: pytest and unittest.mock

# Development Phases

## Part 1: Cloud Ingestion & Database Architecture

* Securely hosted the raw movie, game, and book CSVs (downloaded from Kaggle)
in a cloud data lake using Azure Blob Storage.

* Engineered a Python ETL pipeline utilizing the `azure-storage-blob` SDK to
securely stream raw data into memory.

* Cleaned and standardized the unstructured CSV data using Pandas.

* Spun up a local PostgreSQL instance via Docker and utilized SQLAlchemy to
automatically generate schema tables and bulk-insert the cleaned data.

## Part 2: Vector Math & Machine Learning  

* Activated the pgvector extension inside PostgreSQL to allow native storage of
mathematical arrays.

* Built an independent Machine Learning generation pipeline using
sentence-transformers.

* Downloaded and executed the open-source Hugging Face `all-MiniLM-L6-v2` model
locally to convert English plot summaries into dense, 384-dimensional
mathematical vectors.

* Safely executed bulk UPDATE SQL transactions to cast and store the new Python
arrays as native PostgreSQL vector data types.

## Part 3: The Search Algorithm & FastAPI 

* Engineered a cross-media UNION ALL SQL query utilizing CTEs and pgvector's native <=> operator to calculate Cosine Distance across three distinct tables simultaneously.

* Wrapped the complex database logic into a high-performance, asynchronous REST API using FastAPI.

* Implemented SQLAlchemy parameterization (using the text() function) to securely prevent SQL injections.

## Part 4: Distributed Cloud Deployment

* Architected and deployed a decoupled system consisting of an independent FastAPI
backend and a Streamlit frontend, containerized via Docker and hosted on Azure Container Apps.

* Configured Azure Container Apps for high-availability, serverless execution, 
leveraging managed environment variables.

* Production Deployment Workflow: Engineered a professional CI/CD-ready deployment
workflow, utilizing automated Docker image tagging, multi-stage building, and 
cloud-native environment configuration to ensure environment parity between local development and production.

## Local Setup & Installation

If you wish to run the ETL & Embedding pipelines locally, follow these steps:

1. Clone the Repository
```Bash
git clone https://github.com/OscarKolodziejczyk/Multi-Media-Recommender.git
cd Multi-Media-Recommender
```
2. Environment Variables
   This project requires secure connection strings to run. Create a .env file in
the root directory and populate it with the following structure:

```
# Azure Cloud Credentials

AZURE_STORAGE_CONNECTION_STRING={your_azure_connection_string}
AZURE_CONTAINER_NAME={your_azure_container_name}


# Local PostgreSQL Credentials

DB_USER={your_db_username}
DB_PASSWORD={your_db_password}
DB_HOST="localhost"
DB_PORT="5432"
DB_NAME="juneproject_db" 
```
3. Start up the Database
   Ensure Docker is installed and running on your machine, then execute:

```Bash
docker-compose up -d
```

4. Install Python Dependencies
   It is highly recommended to use a virtual environment.

```Bash
pip install pandas sqlalchemy psycopg2-binary azure-storage-blob
sentence-transformers pgvector python-dotenv pytest
```
5. Execute the Pipelines
   Run the independent pipelines in order to populate your database with semantic math:

```Bash
# 1. Run the isolated test suite
pytest
 
# 2. Pull data from Azure and load into Postgres
python src/ETL/extract_data.py  

# 3. Generate AI vectors and update database rows (this will take several minutes)
python src/Embedding/embedding_pipeline.py 
```
