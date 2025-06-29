# Airflow Docker Setup Guide

## Environment Variables

Create a `.env` file in the same directory as your `docker-compose.yml` with the following variables:

```bash
# Airflow Configuration
AIRFLOW__CORE__FERNET_KEY=your_fernet_key_here

# PostgreSQL Configuration
POSTGRES_USER=airflow
POSTGRES_PASSWORD=your_secure_password_here
POSTGRES_DB=airflow

# Airflow Admin User Configuration
AIRFLOW_ADMIN_USER=admin
AIRFLOW_ADMIN_PASSWORD=your_secure_admin_password_here
AIRFLOW_ADMIN_FIRSTNAME=Airflow
AIRFLOW_ADMIN_LASTNAME=Admin
AIRFLOW_ADMIN_EMAIL=admin@example.com

# Google Cloud Configuration (if using GCP services)
GOOGLE_APPLICATION_CREDENTIALS=/opt/airflow/keys/your-service-account-key.json
```

## Generate Fernet Key

To generate a secure Fernet key, run:

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

## Key Changes Made

1. **Switched to CeleryExecutor**: Now supports distributed task execution
2. **Added Redis Service**: Required for Celery task queue management
3. **Environment Variables**: All sensitive data moved to environment variables
4. **Health Checks**: Added health checks for all services
5. **Restart Policies**: Added restart policies for production reliability
6. **Security**: Removed hardcoded credentials

## Services

- **airflow-webserver**: Web UI (port 8080)
- **airflow-scheduler**: Task scheduler
- **airflow-worker**: Celery worker for task execution
- **postgres**: Database
- **redis**: Message broker for Celery
- **metabase**: Analytics dashboard (port 3000)

## Usage

1. Copy the environment variables above to a `.env` file
2. Generate and set your Fernet key
3. Run: `docker-compose up -d`
4. Access Airflow at: http://localhost:8080
5. Access Metabase at: http://localhost:3000 