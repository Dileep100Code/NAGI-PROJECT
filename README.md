# LPG Connect

**LPG Connect** is a web-based application designed to simplify the management of LPG (Liquefied Petroleum Gas) services including subscription, payments, and delivery tracking. It addresses the inefficiencies of traditional manual systems by providing a centralized digital platform for users and service providers.

## 🛠️ Features

- User registration and login (admin/user)
- Online LPG subscription and plan management
- Secure digital payments and transaction history
- Real-time tracking of orders and next payment dates
- Admin dashboard for monitoring user subscriptions and payments
- Automated reminders and notifications
- Role-based access (user/admin)

## 🧑‍💻 Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Django (Python)
- **Database:** SQLite
- **Authentication:** JWT (JSON Web Tokens)
- **API Framework:** Django REST Framework

## 📁 Project Structure
LPG-Connect/
│
├── backend/                         # Django backend application
│   ├── __init__.py
│   ├── admin.py                     # Admin interface configuration
│   ├── apps.py                      # Django app configuration
│   ├── models.py                    # Database models (UserProfile, Subscription, Payment)
│   ├── serializers.py               # DRF serializers for API responses
│   ├── views.py                     # Core business logic and API endpoints
│   ├── urls.py                      # URL routing for the backend
│   └── tests.py                     # Unit and integration tests
│
├── frontend/                        # Static frontend assets
│   ├── index.html                   # Homepage UI
│   ├── login.html                   # Login page
│   ├── signup.html                  # Signup form
│   ├── dashboard.html               # User/admin dashboards
│   └── styles/                      # CSS files
│       └── main.css
│
├── LPGConnect/                      # Django project folder
│   ├── __init__.py
│   ├── settings.py                  # Project configuration settings
│   ├── urls.py                      # Project-level URL routing
│   └── wsgi.py                      # WSGI application for deployment
│
├── db.sqlite3                       # SQLite database
├── manage.py                        # Django CLI management script
├── requirements.txt                 # Python dependencies
└── README.md                        # Project documentation

