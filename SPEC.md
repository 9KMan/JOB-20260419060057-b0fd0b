# SPEC.md — WhatsApp Loyalty CRM for Car Wash Businesses

## 1. Project Overview

**Project:** WhatsApp Loyalty CRM — Car Wash Businesses (Saudi Arabia)
**Job ID:** JOB-20260419060057-b0fd0b
**Tier:** MICRO
**Stack:** Flask 3.0 + SQLAlchemy 2.0 + Twilio WhatsApp API + PostgreSQL + Docker
**Repository:** https://github.com/9KMan/JOB-20260419060057-b0fd0b

A lightweight WhatsApp-based loyalty and CRM system for car wash businesses in Saudi Arabia. Track customer visits by phone number and automatically reward every 10th wash for free via WhatsApp notifications.

---

## 2. Tech Stack

| Layer       | Technology                                |
|------------|-------------------------------------------|
| Backend     | Flask 3.0, SQLAlchemy 2.0, Flask-CORS  |
| Database    | PostgreSQL 15 (SQLAlchemy ORM)           |
| WhatsApp    | Twilio WhatsApp API (twilio 8.10)       |
| DevOps      | Docker, Docker Compose                   |
| Server      | Gunicorn                                 |
| Testing     | pytest, pytest-flask                     |

---

## 3. Data Models

### Customer
| Column        | Type          | Constraints              |
|--------------|---------------|------------------------|
| id           | Integer (PK) | auto-increment          |
| phone        | String(20)   | UNIQUE, NOT NULL, idx  |
| name         | String(100)  | nullable                |
| total_visits | Integer       | DEFAULT 0               |
| created_at   | DateTime      | DEFAULT utcnow          |
| updated_at   | DateTime      | AUTO on update          |

### Visit
| Column       | Type          | Constraints              |
|-------------|---------------|------------------------|
| id           | Integer (PK) | auto-increment          |
| customer_id  | Integer (FK) | → customers.id          |
| visited_at   | DateTime      | DEFAULT utcnow          |

### Reward
| Column       | Type          | Constraints              |
|-------------|---------------|------------------------|
| id           | Integer (PK) | auto-increment          |
| customer_id  | Integer (FK) | → customers.id          |
| visit_id     | Integer (FK) | → visits.id            |
| rewarded_at  | DateTime      | DEFAULT utcnow          |

---

## 4. Business Logic

### Loyalty Program
- VISITS_PER_REWARD = 10 (configurable via VISITS_PER_REWARD env var)
- Every 10th visit triggers a free wash reward notification via WhatsApp
- Rewards tracked in rewards table

### LoyaltyService
- record_visit(customer) → increment total_visits, check if reward triggered

### WhatsAppService (Twilio)
- send_reward_message(to_phone, customer_name) → send WhatsApp reward notification
- Uses TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_FROM

---

## 5. API Endpoints

- GET /health → health check
- POST /customers → create customer (phone, name)
- GET /customers/phone → get customer by phone
- POST /visits → record a visit (phone), triggers loyalty check → WhatsApp notification on 10th visit
- GET /rewards → list rewards for a customer

---

## 6. Configuration

Environment variables:
DATABASE_URL=postgresql://postgres:password@db:5432/carwash_crm
TWILIO_ACCOUNT_SID=sid
TWILIO_AUTH_TOKEN=token
TWILIO_WHATSAPP_FROM=whatsapp:+1XXXXXXXXXX
VISITS_PER_REWARD=10

---

## 7. File Structure

JOB-20260419060057-b0fd0b/
├── README.md
├── requirements.txt         Flask, SQLAlchemy, Twilio, pytest
├── config.py               Config class (DATABASE_URL, TWILIO_*, VISITS_PER_REWARD)
├── run.py                 app.run() entry point
├── app/
│   ├── __init__.py       create_app()
│   ├── models.py         Customer, Visit, Reward SQLAlchemy models
│   ├── routes.py         All API blueprint routes
│   └── services/
│       ├── __init__.py
│       ├── loyalty_service.py   LoyaltyService (record_visit, reward logic)
│       └── whatsapp_service.py   WhatsAppService (Twilio)
├── docker/
│   ├── Dockerfile         Python 3.12-slim, gunicorn
│   └── docker-compose.yml db (PostgreSQL) + app (Flask)
└── tests/
    ├── __init__.py
    ├── conftest.py
    └── test_loyalty.py   Loyalty logic tests

---

## 8. Docker

Services: db (PostgreSQL 15 Alpine) + app (Flask + Gunicorn)

db: postgres:15-alpine, POSTGRES_DB/carwash_crm, healthcheck pg_isready
app: build ./docker, port 5000, depends_on db, gunicorn server

---

## 9. Quality

- pytest + pytest-flask
- SQLAlchemy ORM with relationship traversal
- Twilio WhatsApp integration (real notification on reward)
- No hardcoded secrets
- Configurable loyalty parameters
