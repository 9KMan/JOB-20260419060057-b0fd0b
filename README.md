# WhatsApp Loyalty CRM for Car Wash Businesses

A lightweight, WhatsApp-based loyalty and CRM system designed for car wash businesses in Saudi Arabia. Track customer visits by phone number and automatically reward every 10th wash for free.

## Features

- **WhatsApp Integration**: Customers interact via WhatsApp messages
- **Phone-based Tracking**: Track visits using customer phone numbers
- **Automatic Rewards**: Every 10th wash is automatically rewarded for free
- **Simple CRM**: Basic customer management with visit history
- **Easy Setup**: Docker-based deployment

## Tech Stack

- **Backend**: Flask 3.0
- **Database**: PostgreSQL with SQLAlchemy ORM
- **WhatsApp**: Twilio WhatsApp Business API
- **Testing**: pytest

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Twilio Account (WhatsApp Business API)

### Environment Setup

Create a `.env` file:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/carwash_crm
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
```

### Run with Docker

```bash
cd docker
docker-compose up -d
```

### Local Development

```bash
pip install -r requirements.txt
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/carwash_crm
flask run --host=0.0.0.0 --port=5000
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| POST | `/api/customers` | Register customer |
| GET | `/api/customers/<phone>` | Get customer details |
| GET | `/api/customers/<phone>/visits` | Get customer visit history |
| POST | `/api/visits` | Record a new visit |
| GET | `/api/rewards/<phone>` | Get available rewards |
| POST | `/api/rewards/<reward_id>/redeem` | Redeem a reward |

### Example: Record a Visit

```bash
curl -X POST http://localhost:5000/api/visits \
  -H "Content-Type: application/json" \
  -d '{"phone": "+966501234567", "notes": "Full wash + interior cleaning"}'
```

## Loyalty System

- Customers earn 1 visit credit for each car wash
- Every **10th visit** earns a FREE car wash reward
- Rewards are automatically created and WhatsApp notification is sent
- Rewards can be redeemed on the next visit

## Project Structure

```
carwash-crm/
├── app/
│   ├── __init__.py      # Flask app factory
│   ├── models.py        # SQLAlchemy models
│   ├── routes.py        # API routes
│   └── services/
│       ├── loyalty_service.py    # Loyalty logic
│       └── whatsapp_service.py    # WhatsApp/Twilio integration
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── tests/
│   └── test_loyalty.py
├── requirements.txt
└── README.md
```

## Testing

```bash
pytest tests/ -v
```

## License

MIT