# gym-back

Backend REST API for gym management, built with Django and Django REST Framework.

## Overview

This project provides a RESTful API to manage gyms (companies), their members (students), offered modalities (classes/activities), financial transactions, staff management, and products. It follows **Domain-Driven Design (DDD)** principles, organized into bounded contexts.

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Framework | Django 5.2.7 |
| REST API | Django REST Framework 3.16.1 |
| Database | PostgreSQL (`psycopg2-binary`) |
| API Docs | drf-yasg (Swagger / ReDoc) |
| Config | python-decouple |
| Server | Gunicorn |
| Reverse Proxy | Nginx |
| Containerization | Docker / Docker Compose |

---

## Architecture

### DDD Context Map

The application is structured around **6 bounded contexts**, each representing a distinct domain with clear responsibilities and boundaries.

```
╔══════════════════════════════════════════════════════════════════════════╗
║                       GYM MANAGEMENT SYSTEM                             ║
║                       Matriz DDD — Context Map                          ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║   ┌──────────────────────────────────────────────────────────────────┐  ║
║   │              Academia / Empresa  [CORE DOMAIN]                   │  ║
║   │  Aggregates: Company                                             │  ║
║   │  API: /api/companies/                                            │  ║
║   └────────────────────────┬─────────────────────────────────────────┘  ║
║            Upstream (U)    │   All other contexts are DOWNSTREAM (D)    ║
║                            │                                             ║
║        ┌───────────────────┼──────────────────────┐                     ║
║        │           ┌───────┴──────┐               │                     ║
║        ▼           ▼              ▼                ▼                     ║
║   ┌─────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐               ║
║   │  Alunos │ │Modalidades│ │Financeiro│ │Administrativo│               ║
║   │(Students│ │(Modali-  │ │(Financial│ │(Admin)       │               ║
║   │   )     │ │ties)     │ │)         │ │              │               ║
║   └────┬────┘ └─────┬────┘ └────┬─────┘ └──────────────┘               ║
║        │   ACL       │           │                                       ║
║        └─────────────┘           │                                       ║
║   Enrollment (N:M)               │                                       ║
║                                  │                                       ║
║                         ┌────────┴──────┐                               ║
║                         │    Produtos   │                               ║
║                         │  (Products)   │                               ║
║                         └───────────────┘                               ║
╚══════════════════════════════════════════════════════════════════════════╝
```

### Context Relationships

| Upstream Context | Downstream Context | Relationship Type | Description |
|---|---|---|---|
| Academia/Empresa | Alunos | Customer/Supplier | Students belong to a Company |
| Academia/Empresa | Modalidades | Customer/Supplier | Modalities are offered by a Company |
| Academia/Empresa | Financeiro | Customer/Supplier | Payments are linked to a Company |
| Academia/Empresa | Administrativo | Customer/Supplier | Staff are employed by a Company |
| Academia/Empresa | Produtos | Customer/Supplier | Products are sold by a Company |
| Alunos | Modalidades | Partnership (ACL) | Students enroll in Modalities |
| Alunos | Financeiro | Customer/Supplier | Students make payments (Subscriptions) |
| Produtos | Financeiro | Customer/Supplier | Products can be sold via payments |
| Administrativo | Alunos | Conformist | Staff are modeled as Students with elevated roles |

> **ACL** = Anti-Corruption Layer — each context references others by ID only (no direct FK), preventing tight coupling.

### Infrastructure Layers

Each bounded context follows the same 4-layer DDD architecture:

```
┌─────────────────────────────────────────┐
│          Interface Layer                │
│  views.py · serializers.py · urls.py   │
├─────────────────────────────────────────┤
│         Application Layer               │
│       application/use_cases.py          │
├─────────────────────────────────────────┤
│           Domain Layer                  │
│  domain/entities.py · domain/services.py│
├─────────────────────────────────────────┤
│        Infrastructure Layer             │
│    infrastructure/repositories.py       │
│          models.py (ORM)               │
└─────────────────────────────────────────┘
```

### Deployment Architecture

```
Internet → Nginx (port 80) → Gunicorn (port 8000) → Django App → PostgreSQL (port 5432)
```

---

## Bounded Contexts

### 1. Academia / Empresa — `company/`

**Type:** Core Domain  
**Responsibility:** Manage the gym or fitness company entity.

| Layer | File | Description |
|---|---|---|
| Domain | `company/domain/entities.py` | `CompanyEntity` aggregate root |
| Domain | `company/domain/services.py` | Payment date calculation, document validation |
| Application | `company/application/use_cases.py` | Create/Get/List/Update/Delete company |
| Infrastructure | `company/infrastructure/repositories.py` | `CompanyRepository` (ORM) |
| Interface | `company/models.py` | Django ORM model |
| Interface | `company/serializers.py` | DRF serializer |
| Interface | `company/views.py` | `CompanyViewSet` |
| Interface | `company/urls.py` | `/api/companies/` |

**Aggregate:** `Company`  
**Key Fields:** `name`, `email`, `document`, `status`, `day_of_payment`, `status_payment`, `next_date_payment`, `last_date_payment`

---

### 2. Alunos — `students/`

**Type:** Supporting Domain  
**Responsibility:** Manage gym members (clients, trainers, admins).

| Layer | File | Description |
|---|---|---|
| Domain | `students/domain/entities.py` | `StudentEntity` aggregate root |
| Domain | `students/domain/services.py` | Email validation, password hashing, enrollment rules |
| Application | `students/application/use_cases.py` | Create/Get/List/Enroll/Update student |
| Infrastructure | `students/infrastructure/repositories.py` | `StudentRepository` (ORM) |
| Interface | `students/models.py` | Django ORM model |
| Interface | `students/serializers.py` | DRF serializer |
| Interface | `students/views.py` | `StudentViewSet` |
| Interface | `students/urls.py` | `/api/students/` |

**Aggregate:** `Student`  
**Key Fields:** `full_name`, `email`, `level` (`client`/`admin`/`personal`), `status`, `company_id`

---

### 3. Modalidades — `modalities/`

**Type:** Supporting Domain  
**Responsibility:** Manage gym activities and classes.

| Layer | File | Description |
|---|---|---|
| Domain | `modalities/domain/entities.py` | `ModalityEntity` aggregate root |
| Domain | `modalities/domain/services.py` | Enrollment capacity rules |
| Application | `modalities/application/use_cases.py` | Create/Get/List/Update modality |
| Infrastructure | `modalities/infrastructure/repositories.py` | `ModalityRepository` (ORM) |
| Interface | `modalities/models.py` | Django ORM model |
| Interface | `modalities/serializers.py` | DRF serializer |
| Interface | `modalities/views.py` | `ModalityViewSet` |
| Interface | `modalities/urls.py` | `/api/modalities/` |

**Aggregate:** `Modality`  
**Key Fields:** `name`, `description`, `status`, `max_capacity`, `company_id`

---

### 4. Financeiro — `financial/`

**Type:** Supporting Domain  
**Responsibility:** Handle payments, subscriptions, and billing.

| Layer | File | Description |
|---|---|---|
| Domain | `financial/domain/entities.py` | `PaymentEntity`, `SubscriptionEntity` |
| Domain | `financial/domain/services.py` | Billing date calculation, discount/late fee logic |
| Application | `financial/application/use_cases.py` | Create/Pay/List payments; Create/Cancel subscriptions |
| Infrastructure | `financial/infrastructure/repositories.py` | `PaymentRepository`, `SubscriptionRepository` |
| Interface | `financial/models.py` | `Payment`, `Subscription` Django ORM models |
| Interface | `financial/serializers.py` | DRF serializers |
| Interface | `financial/views.py` | `PaymentViewSet`, `SubscriptionViewSet` |
| Interface | `financial/urls.py` | `/api/payments/`, `/api/subscriptions/` |

**Aggregates:** `Payment`, `Subscription`  
**Key Fields (Payment):** `amount`, `status` (`pending`/`paid`/`overdue`/`cancelled`), `payment_method`, `due_date`, `paid_at`  
**Key Fields (Subscription):** `plan_name`, `amount`, `billing_cycle` (`monthly`/`quarterly`/`yearly`), `status`, `next_billing_date`

---

### 5. Administrativo — `administrative/`

**Type:** Supporting Domain  
**Responsibility:** Manage staff roles and permissions.

| Layer | File | Description |
|---|---|---|
| Domain | `administrative/domain/entities.py` | `StaffEntity`, `RoleEntity` |
| Domain | `administrative/domain/services.py` | Permission checks per role |
| Application | `administrative/application/use_cases.py` | Create/List/Fire staff; Create/Assign roles |
| Infrastructure | `administrative/infrastructure/repositories.py` | `StaffRepository`, `RoleRepository` |
| Interface | `administrative/models.py` | `Staff`, `Role` Django ORM models |
| Interface | `administrative/serializers.py` | DRF serializers |
| Interface | `administrative/views.py` | `StaffViewSet`, `RoleViewSet` |
| Interface | `administrative/urls.py` | `/api/staff/`, `/api/roles/` |

**Aggregates:** `Staff`, `Role`  
**Key Fields (Staff):** `company_id`, `student_id`, `role`, `status`, `hired_at`, `fired_at`  
**Key Fields (Role):** `name`, `permissions` (JSON list)

---

### 6. Produtos — `products/`

**Type:** Generic Subdomain  
**Responsibility:** Manage products and inventory sold by the gym.

| Layer | File | Description |
|---|---|---|
| Domain | `products/domain/entities.py` | `ProductEntity`, `CategoryEntity` |
| Domain | `products/domain/services.py` | Price calculation, stock validation |
| Application | `products/application/use_cases.py` | Create/Get/List products; Update stock |
| Infrastructure | `products/infrastructure/repositories.py` | `ProductRepository`, `CategoryRepository` |
| Interface | `products/models.py` | `Product`, `Category` Django ORM models |
| Interface | `products/serializers.py` | DRF serializers |
| Interface | `products/views.py` | `ProductViewSet`, `CategoryViewSet` |
| Interface | `products/urls.py` | `/api/products/`, `/api/categories/` |

**Aggregates:** `Product`, `Category`  
**Key Fields (Product):** `name`, `price`, `stock`, `status`, `sku`, `company_id`, `category`

---

## Project Structure

```
gym-back/
├── core/                        # Django project configuration
│   ├── settings.py
│   ├── urls.py                  # Root URL config + Swagger routes
│   ├── wsgi.py
│   └── asgi.py
│
├── company/                     # Bounded Context: Academia/Empresa [CORE]
│   ├── domain/
│   │   ├── entities.py          # CompanyEntity (aggregate root)
│   │   └── services.py          # CompanyDomainService
│   ├── application/
│   │   └── use_cases.py         # CreateCompany, GetCompany, etc.
│   ├── infrastructure/
│   │   └── repositories.py      # CompanyRepository
│   ├── migrations/
│   ├── models.py                # Company ORM model
│   ├── serializers.py
│   ├── views.py                 # CompanyViewSet
│   ├── urls.py                  # /api/companies/
│   └── admin.py
│
├── students/                    # Bounded Context: Alunos
│   ├── domain/
│   │   ├── entities.py          # StudentEntity
│   │   └── services.py          # StudentDomainService
│   ├── application/
│   │   └── use_cases.py         # CreateStudent, EnrollStudent, etc.
│   ├── infrastructure/
│   │   └── repositories.py      # StudentRepository
│   ├── migrations/
│   ├── models.py                # Student ORM model
│   ├── serializers.py
│   ├── views.py                 # StudentViewSet
│   ├── urls.py                  # /api/students/
│   └── admin.py
│
├── modalities/                  # Bounded Context: Modalidades
│   ├── domain/
│   │   ├── entities.py          # ModalityEntity
│   │   └── services.py          # ModalityDomainService
│   ├── application/
│   │   └── use_cases.py         # CreateModality, ListModalities, etc.
│   ├── infrastructure/
│   │   └── repositories.py      # ModalityRepository
│   ├── migrations/
│   ├── models.py                # Modality ORM model
│   ├── serializers.py
│   ├── views.py                 # ModalityViewSet
│   ├── urls.py                  # /api/modalities/
│   └── admin.py
│
├── financial/                   # Bounded Context: Financeiro
│   ├── domain/
│   │   ├── entities.py          # PaymentEntity, SubscriptionEntity
│   │   └── services.py          # FinancialDomainService
│   ├── application/
│   │   └── use_cases.py         # CreatePayment, MarkPaid, CreateSubscription, etc.
│   ├── infrastructure/
│   │   └── repositories.py      # PaymentRepository, SubscriptionRepository
│   ├── migrations/
│   ├── models.py                # Payment, Subscription ORM models
│   ├── serializers.py
│   ├── views.py                 # PaymentViewSet, SubscriptionViewSet
│   ├── urls.py                  # /api/payments/, /api/subscriptions/
│   └── admin.py
│
├── administrative/              # Bounded Context: Administrativo
│   ├── domain/
│   │   ├── entities.py          # StaffEntity, RoleEntity
│   │   └── services.py          # AdministrativeDomainService
│   ├── application/
│   │   └── use_cases.py         # CreateStaff, AssignRole, FireStaff, etc.
│   ├── infrastructure/
│   │   └── repositories.py      # StaffRepository, RoleRepository
│   ├── migrations/
│   ├── models.py                # Staff, Role ORM models
│   ├── serializers.py
│   ├── views.py                 # StaffViewSet, RoleViewSet
│   ├── urls.py                  # /api/staff/, /api/roles/
│   └── admin.py
│
├── products/                    # Bounded Context: Produtos
│   ├── domain/
│   │   ├── entities.py          # ProductEntity, CategoryEntity
│   │   └── services.py          # ProductDomainService
│   ├── application/
│   │   └── use_cases.py         # CreateProduct, UpdateStock, etc.
│   ├── infrastructure/
│   │   └── repositories.py      # ProductRepository, CategoryRepository
│   ├── migrations/
│   ├── models.py                # Product, Category ORM models
│   ├── serializers.py
│   ├── views.py                 # ProductViewSet, CategoryViewSet
│   ├── urls.py                  # /api/products/, /api/categories/
│   └── admin.py
│
├── gym/                         # Legacy monolithic app (kept for reference)
│   └── ...
│
├── nginx/
│   └── nginx.conf               # Reverse proxy configuration
├── Dockerfile
├── docker-compose.yml
├── manage.py
└── requirements.txt
```

---

## API Endpoints

All endpoints are prefixed with `/api/`. Each resource supports standard CRUD operations via Django REST Framework `ModelViewSet`.

### Endpoint Summary

| Domain | Resource | Base URL | Supported Methods |
|---|---|---|---|
| Academia/Empresa | Companies | `/api/companies/` | GET, POST, PUT, PATCH, DELETE |
| Alunos | Students | `/api/students/` | GET, POST, PUT, PATCH, DELETE |
| Alunos | Enrollments | `/api/enrollments/` | GET, POST, PUT, PATCH, DELETE |
| Modalidades | Modalities | `/api/modalities/` | GET, POST, PUT, PATCH, DELETE |
| Financeiro | Payments | `/api/payments/` | GET, POST, PUT, PATCH, DELETE |
| Financeiro | Subscriptions | `/api/subscriptions/` | GET, POST, PUT, PATCH, DELETE |
| Administrativo | Staff | `/api/staff/` | GET, POST, PUT, PATCH, DELETE |
| Administrativo | Roles | `/api/roles/` | GET, POST, PUT, PATCH, DELETE |
| Produtos | Products | `/api/products/` | GET, POST, PUT, PATCH, DELETE |
| Produtos | Categories | `/api/categories/` | GET, POST, PUT, PATCH, DELETE |

### URL Patterns

Each resource follows these URL patterns:

| Method | URL | Description |
|---|---|---|
| `GET` | `/api/<resource>/` | List all records |
| `POST` | `/api/<resource>/` | Create a new record |
| `GET` | `/api/<resource>/{id}/` | Retrieve a record by ID |
| `PUT` | `/api/<resource>/{id}/` | Full update of a record |
| `PATCH` | `/api/<resource>/{id}/` | Partial update of a record |
| `DELETE` | `/api/<resource>/{id}/` | Delete a record |

---

## Detailed Endpoint Reference

### Companies — `/api/companies/`

#### `GET /api/companies/`

Returns a list of all active companies.

**Response `200 OK`:**
```json
[
  {
    "id": 1,
    "name": "Academia FitLife",
    "type_document": "CNPJ",
    "document": "12.345.678/0001-99",
    "status": "active",
    "email": "contato@fitlife.com",
    "foundation_date": "2020-01-15T00:00:00Z",
    "logo": "https://cdn.example.com/logos/fitlife.png",
    "phone_number": "11999990000",
    "avatar_url": null,
    "day_of_payment": 10,
    "next_date_payment": "2026-04-10T00:00:00Z",
    "last_date_payment": "2026-03-10T00:00:00Z",
    "status_payment": "paid",
    "created_at": "2026-01-01T10:00:00Z",
    "updated_at": "2026-03-01T10:00:00Z",
    "deleted_at": null
  }
]
```

#### `POST /api/companies/`

Creates a new company. `next_date_payment` and `last_date_payment` are auto-calculated from `day_of_payment`.

**Request Body:**
```json
{
  "name": "Academia FitLife",
  "type_document": "CNPJ",
  "document": "12.345.678/0001-99",
  "status": "active",
  "email": "contato@fitlife.com",
  "foundation_date": "2020-01-15T00:00:00Z",
  "logo": "https://cdn.example.com/logos/fitlife.png",
  "phone_number": "11999990000",
  "avatar_url": null,
  "day_of_payment": 10,
  "status_payment": "paid"
}
```

**Response `201 Created`:**
```json
{
  "id": 1,
  "name": "Academia FitLife",
  "type_document": "CNPJ",
  "document": "12.345.678/0001-99",
  "status": "active",
  "email": "contato@fitlife.com",
  "foundation_date": "2020-01-15T00:00:00Z",
  "logo": "https://cdn.example.com/logos/fitlife.png",
  "phone_number": "11999990000",
  "avatar_url": null,
  "day_of_payment": 10,
  "next_date_payment": "2026-04-10T00:00:00Z",
  "last_date_payment": "2026-03-10T00:00:00Z",
  "status_payment": "paid",
  "created_at": "2026-03-07T10:00:00Z",
  "updated_at": "2026-03-07T10:00:00Z",
  "deleted_at": null
}
```

#### `GET /api/companies/{id}/`

Returns a single company by ID.

**Response `200 OK`:** Same structure as the list item above.

#### `PUT /api/companies/{id}/`

Full update of a company. All required fields must be provided.

**Request Body:** Same as `POST`.

**Response `200 OK`:** Updated company object.

#### `PATCH /api/companies/{id}/`

Partial update of a company. Only include the fields to update.

**Request Body (example):**
```json
{
  "status": "inactive",
  "status_payment": "overdue"
}
```

**Response `200 OK`:** Updated company object.

#### `DELETE /api/companies/{id}/`

Deletes a company.

**Response `204 No Content`**

**Field Reference:**

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | ✅ | Company name |
| `email` | string (email) | ✅ | Contact email |
| `day_of_payment` | integer | ✅ | Day of month for billing (1–31) |
| `status_payment` | string | ✅ | `paid` / `pending` / `overdue` |
| `type_document` | string | ❌ | Document type (e.g., `CNPJ`) |
| `document` | string | ❌ | Document number |
| `status` | string | ❌ | `active` / `inactive` / `suspended` |
| `foundation_date` | datetime | ❌ | ISO 8601 date |
| `logo` | string | ❌ | URL of the company logo |
| `phone_number` | string | ❌ | Contact phone number |
| `avatar_url` | string | ❌ | URL of the company avatar |
| `next_date_payment` | datetime | 🔒 read-only | Auto-calculated |
| `last_date_payment` | datetime | 🔒 read-only | Auto-calculated |

---

### Students — `/api/students/`

#### `GET /api/students/`

Returns a list of all students.

**Response `200 OK`:**
```json
[
  {
    "id": 1,
    "company_id": 1,
    "full_name": "João Silva",
    "email": "joao.silva@email.com",
    "status": "active",
    "level": "client",
    "document": "123.456.789-00",
    "date_of_birth": "1995-06-20T00:00:00Z",
    "phone_number": "11988880000",
    "gender": "male",
    "avatar_url": null,
    "created_at": "2026-01-10T08:00:00Z",
    "updated_at": "2026-03-01T10:00:00Z"
  }
]
```

#### `POST /api/students/`

Creates a new student. `password` is write-only.

**Request Body:**
```json
{
  "company_id": 1,
  "full_name": "João Silva",
  "email": "joao.silva@email.com",
  "password": "securepassword123",
  "status": "active",
  "level": "client",
  "document": "123.456.789-00",
  "date_of_birth": "1995-06-20T00:00:00Z",
  "phone_number": "11988880000",
  "gender": "male",
  "avatar_url": null
}
```

**Response `201 Created`:**
```json
{
  "id": 1,
  "company_id": 1,
  "full_name": "João Silva",
  "email": "joao.silva@email.com",
  "status": "active",
  "level": "client",
  "document": "123.456.789-00",
  "date_of_birth": "1995-06-20T00:00:00Z",
  "phone_number": "11988880000",
  "gender": "male",
  "avatar_url": null,
  "created_at": "2026-03-07T10:00:00Z",
  "updated_at": "2026-03-07T10:00:00Z"
}
```

**Field Reference:**

| Field | Type | Required | Description |
|---|---|---|---|
| `company_id` | integer | ✅ | ID of the owning company |
| `full_name` | string | ✅ | Student's full name |
| `email` | string (email) | ✅ | Unique email address |
| `password` | string | ✅ | Password (write-only) |
| `status` | string | ❌ | `active` / `inactive` |
| `level` | string | ❌ | `client` / `admin` / `personal` |
| `document` | string | ❌ | CPF or other document |
| `date_of_birth` | datetime | ❌ | ISO 8601 date |
| `phone_number` | string | ❌ | Contact phone number |
| `gender` | string | ❌ | Gender |
| `avatar_url` | string | ❌ | URL of profile picture |

---

### Enrollments — `/api/enrollments/`

#### `GET /api/enrollments/`

Returns a list of all active enrollments.

**Response `200 OK`:**
```json
[
  {
    "id": 1,
    "student": 1,
    "modality_id": 3,
    "enrolled_at": "2026-02-01T09:00:00Z",
    "active": true
  }
]
```

#### `POST /api/enrollments/`

Enrolls a student in a modality.

**Request Body:**
```json
{
  "student": 1,
  "modality_id": 3,
  "active": true
}
```

**Response `201 Created`:**
```json
{
  "id": 1,
  "student": 1,
  "modality_id": 3,
  "enrolled_at": "2026-03-07T10:00:00Z",
  "active": true
}
```

**Field Reference:**

| Field | Type | Required | Description |
|---|---|---|---|
| `student` | integer | ✅ | ID of the student |
| `modality_id` | integer | ✅ | ID of the modality |
| `active` | boolean | ❌ | Defaults to `true` |
| `enrolled_at` | datetime | 🔒 read-only | Auto-set on creation |

---

### Modalities — `/api/modalities/`

#### `GET /api/modalities/`

Returns a list of all active (non-deleted) modalities.

**Response `200 OK`:**
```json
[
  {
    "id": 1,
    "company_id": 1,
    "name": "Musculação",
    "description": "Treino de força com equipamentos",
    "status": "active",
    "max_capacity": 30,
    "created_at": "2026-01-05T08:00:00Z",
    "updated_at": "2026-01-05T08:00:00Z",
    "deleted_at": null
  }
]
```

#### `POST /api/modalities/`

Creates a new modality.

**Request Body:**
```json
{
  "company_id": 1,
  "name": "Musculação",
  "description": "Treino de força com equipamentos",
  "status": "active",
  "max_capacity": 30
}
```

**Response `201 Created`:**
```json
{
  "id": 1,
  "company_id": 1,
  "name": "Musculação",
  "description": "Treino de força com equipamentos",
  "status": "active",
  "max_capacity": 30,
  "created_at": "2026-03-07T10:00:00Z",
  "updated_at": "2026-03-07T10:00:00Z",
  "deleted_at": null
}
```

**Field Reference:**

| Field | Type | Required | Description |
|---|---|---|---|
| `company_id` | integer | ✅ | ID of the owning company |
| `name` | string | ✅ | Modality name |
| `description` | string | ❌ | Detailed description |
| `status` | string | ❌ | `active` / `inactive` (default: `active`) |
| `max_capacity` | integer | ❌ | Maximum number of enrolled students |

---

### Payments — `/api/payments/`

#### `GET /api/payments/`

Returns a list of all payments.

**Response `200 OK`:**
```json
[
  {
    "id": 1,
    "company_id": 1,
    "student_id": 1,
    "amount": "150.00",
    "status": "pending",
    "payment_method": "pix",
    "due_date": "2026-04-10T00:00:00Z",
    "paid_at": null,
    "description": "Mensalidade Março/2026",
    "created_at": "2026-03-07T10:00:00Z",
    "updated_at": "2026-03-07T10:00:00Z"
  }
]
```

#### `POST /api/payments/`

Creates a new payment record.

**Request Body:**
```json
{
  "company_id": 1,
  "student_id": 1,
  "amount": "150.00",
  "status": "pending",
  "payment_method": "pix",
  "due_date": "2026-04-10T00:00:00Z",
  "description": "Mensalidade Março/2026"
}
```

**Response `201 Created`:**
```json
{
  "id": 1,
  "company_id": 1,
  "student_id": 1,
  "amount": "150.00",
  "status": "pending",
  "payment_method": "pix",
  "due_date": "2026-04-10T00:00:00Z",
  "paid_at": null,
  "description": "Mensalidade Março/2026",
  "created_at": "2026-03-07T10:00:00Z",
  "updated_at": "2026-03-07T10:00:00Z"
}
```

**Field Reference:**

| Field | Type | Required | Description |
|---|---|---|---|
| `company_id` | integer | ✅ | ID of the company |
| `student_id` | integer | ✅ | ID of the student |
| `amount` | decimal | ✅ | Payment amount |
| `status` | string | ❌ | `pending` / `paid` / `overdue` / `cancelled` (default: `pending`) |
| `payment_method` | string | ❌ | `cash` / `card` / `pix` / `transfer` |
| `due_date` | datetime | ❌ | Payment due date |
| `paid_at` | datetime | 🔒 read-only | Set when payment is marked as paid |
| `description` | string | ❌ | Description of the payment |

---

### Subscriptions — `/api/subscriptions/`

#### `GET /api/subscriptions/`

Returns a list of all active subscriptions.

**Response `200 OK`:**
```json
[
  {
    "id": 1,
    "company_id": 1,
    "student_id": 1,
    "plan_name": "Plano Mensal",
    "amount": "120.00",
    "billing_cycle": "monthly",
    "status": "active",
    "start_date": "2026-01-01T00:00:00Z",
    "end_date": null,
    "next_billing_date": "2026-04-01T00:00:00Z",
    "created_at": "2026-01-01T10:00:00Z",
    "updated_at": "2026-03-01T10:00:00Z"
  }
]
```

#### `POST /api/subscriptions/`

Creates a new subscription.

**Request Body:**
```json
{
  "company_id": 1,
  "student_id": 1,
  "plan_name": "Plano Mensal",
  "amount": "120.00",
  "billing_cycle": "monthly",
  "status": "active",
  "start_date": "2026-01-01T00:00:00Z",
  "end_date": null
}
```

**Response `201 Created`:**
```json
{
  "id": 1,
  "company_id": 1,
  "student_id": 1,
  "plan_name": "Plano Mensal",
  "amount": "120.00",
  "billing_cycle": "monthly",
  "status": "active",
  "start_date": "2026-01-01T00:00:00Z",
  "end_date": null,
  "next_billing_date": "2026-04-01T00:00:00Z",
  "created_at": "2026-03-07T10:00:00Z",
  "updated_at": "2026-03-07T10:00:00Z"
}
```

**Field Reference:**

| Field | Type | Required | Description |
|---|---|---|---|
| `company_id` | integer | ✅ | ID of the company |
| `student_id` | integer | ✅ | ID of the student |
| `plan_name` | string | ✅ | Name of the subscription plan |
| `amount` | decimal | ✅ | Recurring billing amount |
| `billing_cycle` | string | ❌ | `monthly` / `quarterly` / `yearly` (default: `monthly`) |
| `status` | string | ❌ | `active` / `cancelled` / `suspended` (default: `active`) |
| `start_date` | datetime | ❌ | Subscription start date |
| `end_date` | datetime | ❌ | Subscription end date (null = ongoing) |
| `next_billing_date` | datetime | 🔒 read-only | Auto-calculated based on billing cycle |

---

### Staff — `/api/staff/`

#### `GET /api/staff/`

Returns a list of all active staff members.

**Response `200 OK`:**
```json
[
  {
    "id": 1,
    "company_id": 1,
    "student_id": 2,
    "role": 1,
    "status": "active",
    "hired_at": "2025-03-01T00:00:00Z",
    "fired_at": null,
    "created_at": "2025-03-01T08:00:00Z",
    "updated_at": "2026-01-10T10:00:00Z"
  }
]
```

#### `POST /api/staff/`

Registers a new staff member.

**Request Body:**
```json
{
  "company_id": 1,
  "student_id": 2,
  "role": 1,
  "status": "active",
  "hired_at": "2025-03-01T00:00:00Z"
}
```

**Response `201 Created`:**
```json
{
  "id": 1,
  "company_id": 1,
  "student_id": 2,
  "role": 1,
  "status": "active",
  "hired_at": "2025-03-01T00:00:00Z",
  "fired_at": null,
  "created_at": "2026-03-07T10:00:00Z",
  "updated_at": "2026-03-07T10:00:00Z"
}
```

**Field Reference:**

| Field | Type | Required | Description |
|---|---|---|---|
| `company_id` | integer | ✅ | ID of the company |
| `student_id` | integer | ✅ | ID of the student (staff member) |
| `role` | integer | ❌ | ID of the role assigned |
| `status` | string | ❌ | `active` / `inactive` (default: `active`) |
| `hired_at` | datetime | ❌ | Date the staff member was hired |
| `fired_at` | datetime | ❌ | Date the staff member was dismissed |

---

### Roles — `/api/roles/`

#### `GET /api/roles/`

Returns a list of all roles.

**Response `200 OK`:**
```json
[
  {
    "id": 1,
    "name": "Personal Trainer",
    "description": "Instrutor de treino personalizado",
    "permissions": ["view_students", "manage_enrollments"],
    "created_at": "2026-01-01T08:00:00Z",
    "updated_at": "2026-01-01T08:00:00Z"
  }
]
```

#### `POST /api/roles/`

Creates a new role.

**Request Body:**
```json
{
  "name": "Personal Trainer",
  "description": "Instrutor de treino personalizado",
  "permissions": ["view_students", "manage_enrollments"]
}
```

**Response `201 Created`:**
```json
{
  "id": 1,
  "name": "Personal Trainer",
  "description": "Instrutor de treino personalizado",
  "permissions": ["view_students", "manage_enrollments"],
  "created_at": "2026-03-07T10:00:00Z",
  "updated_at": "2026-03-07T10:00:00Z"
}
```

**Field Reference:**

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | ✅ | Unique role name |
| `description` | string | ❌ | Role description |
| `permissions` | array of strings | ❌ | List of permission identifiers |

---

### Products — `/api/products/`

#### `GET /api/products/`

Returns a list of all active (non-deleted) products.

**Response `200 OK`:**
```json
[
  {
    "id": 1,
    "company_id": 1,
    "category": 2,
    "name": "Whey Protein 1kg",
    "description": "Suplemento proteico sabor baunilha",
    "price": "89.90",
    "stock": 50,
    "status": "active",
    "sku": "WP-VAN-1KG",
    "image_url": "https://cdn.example.com/products/whey.png",
    "created_at": "2026-02-01T08:00:00Z",
    "updated_at": "2026-02-15T10:00:00Z",
    "deleted_at": null
  }
]
```

#### `POST /api/products/`

Creates a new product.

**Request Body:**
```json
{
  "company_id": 1,
  "category": 2,
  "name": "Whey Protein 1kg",
  "description": "Suplemento proteico sabor baunilha",
  "price": "89.90",
  "stock": 50,
  "status": "active",
  "sku": "WP-VAN-1KG",
  "image_url": "https://cdn.example.com/products/whey.png"
}
```

**Response `201 Created`:**
```json
{
  "id": 1,
  "company_id": 1,
  "category": 2,
  "name": "Whey Protein 1kg",
  "description": "Suplemento proteico sabor baunilha",
  "price": "89.90",
  "stock": 50,
  "status": "active",
  "sku": "WP-VAN-1KG",
  "image_url": "https://cdn.example.com/products/whey.png",
  "created_at": "2026-03-07T10:00:00Z",
  "updated_at": "2026-03-07T10:00:00Z",
  "deleted_at": null
}
```

**Field Reference:**

| Field | Type | Required | Description |
|---|---|---|---|
| `company_id` | integer | ✅ | ID of the owning company |
| `name` | string | ✅ | Product name |
| `price` | decimal | ✅ | Product price |
| `category` | integer | ❌ | ID of the product category |
| `description` | string | ❌ | Product description |
| `stock` | integer | ❌ | Available stock quantity (default: `0`) |
| `status` | string | ❌ | `active` / `inactive` / `out_of_stock` (default: `active`) |
| `sku` | string | ❌ | Unique stock-keeping unit identifier |
| `image_url` | string | ❌ | URL of the product image |

---

### Categories — `/api/categories/`

#### `GET /api/categories/`

Returns a list of all categories.

**Response `200 OK`:**
```json
[
  {
    "id": 1,
    "name": "Suplementos",
    "description": "Suplementos alimentares e vitaminas",
    "created_at": "2026-01-01T08:00:00Z",
    "updated_at": "2026-01-01T08:00:00Z"
  }
]
```

#### `POST /api/categories/`

Creates a new product category.

**Request Body:**
```json
{
  "name": "Suplementos",
  "description": "Suplementos alimentares e vitaminas"
}
```

**Response `201 Created`:**
```json
{
  "id": 1,
  "name": "Suplementos",
  "description": "Suplementos alimentares e vitaminas",
  "created_at": "2026-03-07T10:00:00Z",
  "updated_at": "2026-03-07T10:00:00Z"
}
```

**Field Reference:**

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | ✅ | Unique category name |
| `description` | string | ❌ | Category description |

---

### Common Response Codes

| Code | Meaning |
|---|---|
| `200 OK` | Request successful (GET, PUT, PATCH) |
| `201 Created` | Resource successfully created (POST) |
| `204 No Content` | Resource successfully deleted (DELETE) |
| `400 Bad Request` | Validation error — check request body |
| `404 Not Found` | Resource with given ID does not exist |
| `500 Internal Server Error` | Unexpected server error |

**Example `400 Bad Request` response:**
```json
{
  "email": ["This field must be unique."],
  "amount": ["A valid number is required."]
}
```

---

## API Documentation

Interactive documentation is available after starting the server:

| UI | URL |
|---|---|
| Swagger UI | `http://localhost:8000/swagger/` |
| ReDoc | `http://localhost:8000/redoc/` |
| OpenAPI JSON | `http://localhost:8000/swagger.json/` |

---

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

---

### Running with Docker

The project includes a full Docker Compose setup with Nginx, Gunicorn, and PostgreSQL.

1. **Configure environment variables**

   Create a `.env` file as described above, using `DB_HOST=academia_db` to match the Docker service name.

2. **Start all services**
   ```bash
   docker-compose up --build
   ```

3. **Run migrations inside the container**
   ```bash
   docker-compose exec academia_web python manage.py migrate
   ```

The API will be available at `http://localhost/api/` (via Nginx on port 80).

| Service | Container | Port |
|---|---|---|
| Django + Gunicorn | `academia_web` | 8000 (internal) |
| PostgreSQL | `academia_db` | 5438 → 5432 |
| Nginx | `academia_nginx` | 80 |

