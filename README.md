<div align="center">
  <img align="center" src="app/static/images/QuickTD-Icon-1.png" width="200" alt="quick-td logo">
</div>

# Quick TD API

<div align="center">

<!-- ![uv Badge](https://img.shields.io/badge/uv-DE5FE9?logo=uv&logoColor=fff&style=for-the-badge) -->
<!-- ![Ruff Badge](https://img.shields.io/badge/Ruff-D7FF64?logo=ruff&logoColor=000&style=for-the-badge) -->

[![uv Badge](https://img.shields.io/badge/uv-D7FF64?logo=uv&logoColor=261230&style=for-the-badge)](https://github.com/astral-sh/uv)
[![Ruff Badge](https://img.shields.io/badge/Ruff-D7FF64?logo=ruff&color=261230&style=for-the-badge)](https://github.com/astral-sh/ruff)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Pytest](https://img.shields.io/badge/pytest-%23ffffff.svg?style=for-the-badge&logo=pytest&logoColor=2f9fe3)
![Amazon Web Services Badge](https://img.shields.io/badge/Amazon%20Web%20Services-232F3E?logo=amazonwebservices&logoColor=fff&style=for-the-badge)
![AWS Lambda Badge](https://img.shields.io/badge/AWS%20Lambda-F90?logo=awslambda&logoColor=fff&style=for-the-badge)
![Visual Studio Code](https://custom-icon-badges.demolab.com/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=vsc&logoColor=white)
[![Beanie ODM](https://custom-icon-badges.demolab.com/badge/Beanie-000.svg?style=for-the-badge&logo=beanie&logoColor=white&labelColor=000)](https://beanie-odm.dev/)

<!-- <img src="https://raw.githubusercontent.com/roman-right/beanie/main/assets/logo/white_bg.svg" width="100" alt="beanie logo"> -->

</div>

# 📝 Task Manager Backend – Clean Hexagonal FastAPI Project

This is the backend of a task management system for a development team. It is built with **FastAPI** using an architecture based on **Clean Architecture** and **Hexagonal** principles, with deployment prepared for **AWS Lambda**, data handling with **MongoDB**, and its modern ODM **Beanie**.
It is designed to be a simple and fast tool for creating and managing time series databases.

---

## 🚀 Tech Stacks and Tools Used

| Technology                                                  | Purpose                                                |
| ----------------------------------------------------------- | ------------------------------------------------------ |
| [FastAPI](https://fastapi.tiangolo.com/)                    | Modern web framework for building fast, type-safe APIs |
| [Beanie](https://beanie-odm.dev/)                           | ODM for MongoDB using Pydantic v2 and Motor            |
| [MongoDB](https://www.mongodb.com/)                         | NoSQL database                                         |
| [Mangum](https://github.com/jordaneremieff/mangum)          | ASGI adapter for AWS Lambda                            |
| [Scalar](https://scalar.com/)                               | Custom UI to visualize OpenAPI documentation           |
| [Docker](https://www.docker.com/)                           | Containerization for development and deployment        |
| [AWS](https://aws.amazon.com/)                              | Infrastructure to deploy (Lambda, API Gateway, etc.)   |
| [Ruff](https://docs.astral.sh/ruff/)                        | Fast linter and formatter for Python code              |
| [uv](https://docs.astral.sh/uv/)                            | Ultra-fast dependency manager for Python               |
| [Git](https://git-scm.com/) + [GitHub](https://github.com/) | Version control and remote repository management       |

---

## 🗂️ Project Structure

```txt
app/
├── api/                # HTTP routes exposed via FastAPI
├── core/               # Pure business logic (entities, enums, interfaces)
├── domain/             # Domain models, DTOs
├── infrastructure/     # External adapters (MongoDB, JWT, Passwords)
├── logs/               # Structured logs
├── schemas/            # Pydantic schemas for validation and documentation
├── services/           # Use cases and application logic
├── static/             # Static files (e.g., Scalar OpenAPI UI)
├── utils/              # Common helpers and utilities
├── main.py             # Entry point for local / Docker execution
```

## For deployment

aws lambda invoke \
 --function-name quickTDLambda \
 --payload file://event.json \
 --cli-binary-format raw-in-base64-out \
 response.json

aws iam create-role \
--role-name quicktd-api-lambda-role \
 --assume-role-policy-document '{"Version": "2012-10-17", "Statement": [{ "Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}]}'
