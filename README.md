# gym-back

Backend REST API for gym management, built with Django and Django REST Framework.

## Overview

This project provides a RESTful API to manage gyms (companies), their members (users), and offered modalities (classes/activities). It includes auto-generated Swagger/ReDoc documentation.

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Framework | Django 5.2.7 |
| REST API | Django REST Framework 3.16.1 |
| Database | PostgreSQL (`psycopg2-binary`) |
| API Docs | drf-yasg (Swagger / ReDoc) |
| Config | python-decouple |

## Project Structure

```
gym-back/
├── core/                  # Django project configuration
│   ├── settings.py        # Project settings (env-based config)
│   ├── urls.py            # Root URL configuration + Swagger routes
│   ├── wsgi.py            # WSGI entry point
│   └── asgi.py            # ASGI entry point
├── gym/                   # Main application
│   ├── models.py          # Data models (Company, User, Modalitie)
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # ViewSets (CRUD endpoints)
│   ├── urls.py            # App-level URL routing
│   ├── admin.py           # Django admin registration
│   └── migrations/        # Database migrations
├── manage.py              # Django management CLI
└── requirements.txt       # Python dependencies
```

## Data Models

### Company (Gym)
Represents a gym. Fields include `name`, `email`, `document`, `status`, `phone_number`, `logo`, `avatar_url`, `day_of_payment`, `status_payment`, and timestamps (`created_at`, `updated_at`, `deleted_at`). Payment dates (`next_date_payment`, `last_date_payment`) are automatically calculated from `day_of_payment`.

### User
Represents a gym member or staff. Belongs to a `Company` and can be enrolled in multiple `Modalitie`s. Fields include `full_name`, `email`, `password`, `level` (`client`, `admin`, `personal`), `status` (`active`, `inactive`), `document`, `date_of_birth`, `gender`, `phone_number`, and `avatar_url`.

### Modalitie
Represents an activity or class offered by a gym (`Company`). Fields include `name` and `status`.

### Relationships

```
Company  1 ──── N  Modalitie
Company  1 ──── N  User
User     N ──── M  Modalitie
```

## API Endpoints

All endpoints are prefixed with `/api/`.

| Resource | Endpoint |
|---|---|
| Users | `/api/users/` |
| Modalities | `/api/modalities/` |
| Companies | `/api/companies/` |

All resources support standard CRUD operations via DRF `ModelViewSet`:
`GET`, `POST`, `PUT`, `PATCH`, `DELETE`.

## API Documentation

Interactive documentation is available after starting the server:

| UI | URL |
|---|---|
| Swagger UI | `/swagger/` |
| ReDoc | `/redoc/` |
| OpenAPI JSON | `/swagger.json/` |

## Getting Started

### Prerequisites

- Python 3.12+
- PostgreSQL

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/coding-developers/gym-back.git
   cd gym-back
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-secret-key
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   DB_NAME=gym_db
   DB_USER=postgres
   DB_PASSWORD=your-db-password
   DB_HOST=localhost
   DB_PORT=5432
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000/api/`.
