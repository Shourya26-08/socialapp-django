# Dispatch — Mini Social Media Platform

A full-stack social media application built with **Django REST Framework** and a lightweight HTML/CSS/JavaScript frontend.

## Features

- User registration, login and logout
- Token-based authentication
- User profiles with bio and avatar URL
- Create and delete posts
- Global and following-only feeds
- Like and unlike posts
- Add and delete comments
- Follow and unfollow users
- Followers/following lists
- Django admin panel
- SQLite database for simple local setup

## Tech Stack

**Backend:** Python, Django, Django REST Framework, SQLite  
**Frontend:** HTML5, CSS3, JavaScript (Fetch API)  
**Authentication:** DRF Token Authentication  
**API:** RESTful JSON API

## Project Structure

```text
socialapp-django/
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── social_project/
│   └── social/
│       ├── migrations/
│       ├── models.py
│       ├── serializers.py
│       ├── views.py
│       ├── urls.py
│       ├── signals.py
│       └── admin.py
├── frontend/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── profile.html
│   ├── css/style.css
│   └── js/
└── .gitignore
```

## Run Locally

### Backend

```bash
cd backend
python -m venv venv
venv\\Scripts\\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

The API runs at `http://127.0.0.1:8000/api/`.

### Frontend

In a second terminal:

```bash
cd frontend
python -m http.server 5500
```

Open `http://127.0.0.1:5500` in your browser.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/auth/register/` | Register |
| POST | `/api/auth/login/` | Login |
| POST | `/api/auth/logout/` | Logout |
| GET | `/api/auth/me/` | Current profile |
| GET | `/api/posts/` | Feed |
| POST | `/api/posts/` | Create post |
| DELETE | `/api/posts/<id>/` | Delete own post |
| POST/DELETE | `/api/posts/<id>/like/` | Like/unlike |
| GET/POST | `/api/posts/<id>/comments/` | Read/add comments |
| DELETE | `/api/comments/<id>/` | Delete own comment |
| GET | `/api/users/<username>/` | Profile |
| PATCH | `/api/users/me/update/` | Update profile |
| POST/DELETE | `/api/users/<username>/follow/` | Follow/unfollow |

## Security Notes

The repository contains no database, virtual environment, secrets, or generated Python cache files. For production deployment, move `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, and CORS configuration to environment variables.

## Internship Project

This project demonstrates full-stack development, REST API design, authentication, relational data modelling, frontend API integration, and CRUD operations.