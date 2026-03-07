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

---

## DDD Context Map (Matriz DDD)

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
├── manage.py
└── requirements.txt
```

---

## API Endpoints

All endpoints are prefixed with `/api/`.

| Domain | Resource | Endpoint | Methods |
|---|---|---|---|
| Academia/Empresa | Companies | `/api/companies/` | GET, POST, PUT, PATCH, DELETE |
| Alunos | Students | `/api/students/` | GET, POST, PUT, PATCH, DELETE |
| Modalidades | Modalities | `/api/modalities/` | GET, POST, PUT, PATCH, DELETE |
| Financeiro | Payments | `/api/payments/` | GET, POST, PUT, PATCH, DELETE |
| Financeiro | Subscriptions | `/api/subscriptions/` | GET, POST, PUT, PATCH, DELETE |
| Administrativo | Staff | `/api/staff/` | GET, POST, PUT, PATCH, DELETE |
| Administrativo | Roles | `/api/roles/` | GET, POST, PUT, PATCH, DELETE |
| Produtos | Products | `/api/products/` | GET, POST, PUT, PATCH, DELETE |
| Produtos | Categories | `/api/categories/` | GET, POST, PUT, PATCH, DELETE |

---

## API Documentation

Interactive documentation is available after starting the server:

| UI | URL |
|---|---|
| Swagger UI | `/swagger/` |
| ReDoc | `/redoc/` |
| OpenAPI JSON | `/swagger.json/` |

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
