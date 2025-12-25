# 🚀 Employee Management API (FastAPI + Keycloak + PostgreSQL)\
A professional-grade, secure FastAPI application for managing employee records. This project demonstrates Identity Federation by syncing users between Keycloak (Identity Provider) and Postgres (Business Database).

## 🛠️ Features\
-Secure Authentication: JWT Bearer Token verification using Keycloak Public Keys (RSA256).\
-Identity Syncing: Automatically creates users in Keycloak and maps their UID to PostgreSQL.\
-Auto-Login: Generates an access token immediately upon employee registration.\
-Robust Validation: Uses Pydantic for request filtering and Peewee ORM for database constraints.\
-Automated Docs: Full Swagger UI integration with Authorize button support.\

## 🏗️ Tech Stack\
-Backend: FastAPI (Python 3.10+)\
-Database: PostgreSQL\
-ORM: Peewee\
-Identity Provider: Keycloak (OpenID Connect)\
-Server: Uvicorn\

## This is a great foundation! To make this "GitHub Ready," we need to add a bit of visual structure, clear code blocks for the .env setup, and a professional layout.

Since we just moved your secrets to the .env file, I have added a section specifically for that so anyone who downloads your code knows exactly what "keys" they need to provide.

🚀 Employee Management API (FastAPI + Keycloak + PostgreSQL)
A professional-grade, secure FastAPI application for managing employee records. This project demonstrates Identity Federation by syncing users between Keycloak (Identity Provider) and Postgres (Business Database).

🛠️ Features
Secure Authentication: JWT Bearer Token verification using Keycloak Public Keys (RSA256).

Identity Syncing: Automatically creates users in Keycloak and maps their UID to PostgreSQL.

Auto-Login: Generates an access token immediately upon employee registration.

Robust Validation: Uses Pydantic for request filtering and Peewee ORM for database constraints.

Automated Docs: Full Swagger UI integration with Authorize button support.

🏗️ Tech Stack
Backend: FastAPI (Python 3.10+)

Database: PostgreSQL

ORM: Peewee

Identity Provider: Keycloak (OpenID Connect)

Server: Uvicorn

🚦 Getting Started

