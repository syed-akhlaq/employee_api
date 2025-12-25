# 🚀 Employee Management API (FastAPI + Keycloak + PostgreSQL)
A professional-grade, secure FastAPI application for managing employee records. This project demonstrates Identity Federation by syncing users between Keycloak (Identity Provider) and Postgres (Business Database).

## 🛠️ Features
-Secure Authentication: JWT Bearer Token verification using Keycloak Public Keys (RSA256).\
-Identity Syncing: Automatically creates users in Keycloak and maps their UID to PostgreSQL.\
-Auto-Login: Generates an access token immediately upon employee registration.\
-Robust Validation: Uses Pydantic for request filtering and Peewee ORM for database constraints.\
-Automated Docs: Full Swagger UI integration with Authorize button support.

## 🏗️ Tech Stack
-Backend: FastAPI (Python 3.10+)\
-Database: PostgreSQL\
-ORM: Peewee\
-Identity Provider: Keycloak (OpenID Connect)\
-Server: Uvicorn

## 🚦 Getting Started
### 1. Prerequisites
Ensure you have the following installed:\
-Python 3.10+\
-PostgreSQL (Running locally or via Docker)\
-Keycloak (Running on port 8080)

### 2. Installation
Clone the repository and install the dependencies:

-Create a virtual environment
```
Bash

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

-Install requirements
```
Bash

pip install fastapi uvicorn peewee psycopg2-binary python-jose[cryptography] python-dotenv python-keycloak`
```
### 3. Environment Configuration
Create a .env file in the root directory and paste the following, replacing the values with your actual setup:
```
Code snippet

# Database
DB_NAME=employee_mgmt
DB_USER=your_user
DB_PASS=your_password
DB_HOST=localhost
DB_PORT=5432

# Keycloak Admin (to create users)
KC_ADMIN_USER=admin_username
KC_ADMIN_PASS=admin_password

# Keycloak Client Config
KC_SERVER_URL=http://localhost:8080/
KC_REALM=employees
KC_CLIENT_ID=fastapi-client
KC_CLIENT_SECRET=your_client_secret

# Keycloak Verification (Public Key from Realm Settings)
KC_PUBLIC_KEY="MIIBIjANBgkqh..."

```

## 🏃 Running the App
### 1.Start the Server:
```
Bash

uvicorn main:app --reload
```
### 2.Access Documentation: Open http://127.0.0.1:8000/docs in your browser.

## 🔐 How to Authenticate
### Step 1 
Use the POST /employees endpoint. This will:\
1.Create the user in Keycloak.\
2.Save the employee data in Postgres.\
3.Return an access_token in the response.

### Step 2: Authorize in Swagger
1.Copy the access_token from the Step 1 response.\
2.Click the Authorize (padlock) button at the top of the Swagger page.\
3.Paste the token and click Authorize.\
4.You can now access protected GET, PUT, and DELETE routes.

## 📁 Project Structure
-``main.py:`` API routes and application lifecycle.\
-``database.py:`` PostgreSQL connection and Peewee models.\
-``schemas.py:`` Pydantic models for data validation.\
-``security.py:`` JWT decoding and RSA signature verification.\
-``keycloak_utils.py:`` Admin utilities for user management.\
-``.env:`` Secret configuration (do not commit to git!).
















