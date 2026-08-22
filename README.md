# Dispatch — Mini Social Media Platform

A small full-stack social app: user profiles, posts & comments, and a like/follow system.

- **Backend:** Django + Django REST Framework, SQLite database
- **Frontend:** Plain HTML, CSS, and JavaScript (no build step, no framework)
- **Auth:** Token-based (DRF's `TokenAuthentication`)

## Features

- Register / log in / log out
- Profiles with bio + avatar URL, follower/following/post counts
- Create, view, and delete posts (text feed, newest first)
- "Everyone" and "Following" feed tabs
- Comment on posts, delete your own comments
- Like / unlike posts with live counts
- Follow / unfollow users, with followers & following list modals

## Project structure

```
socialapp/
├── backend/                  # Django + DRF API
│   ├── manage.py
│   ├── requirements.txt
│   ├── social_project/        # settings, urls, wsgi/asgi
│   └── social/                 # the app: models, serializers, views, urls
├── frontend/                  # static HTML/CSS/JS client
│   ├── index.html              # feed
│   ├── login.html
│   ├── register.html
│   ├── profile.html
│   ├── css/style.css
│   └── js/ (api.js, ui.js, feed.js, profile.js)
└── README.md
```

## Running it locally

### 1. Backend (Django API — runs on port 8000)

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser   # optional, for /admin/

python manage.py runserver
```

The API is now live at `http://127.0.0.1:8000/api/`, and the Django admin at `http://127.0.0.1:8000/admin/`.

### 2. Frontend (static files — runs on port 5500 or similar)

The frontend is plain static files, so any static server works. From the `frontend/` folder:

```bash
cd frontend
python -m http.server 5500
```

Then open `http://127.0.0.1:5500` in your browser.

> The frontend calls the API at `http://127.0.0.1:8000/api` (see the `API_BASE` constant at the top of `frontend/js/api.js`). If you serve the backend on a different host/port, update that constant.

## API reference

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/api/auth/register/` | Create an account | — |
| POST | `/api/auth/login/` | Log in, get a token | — |
| POST | `/api/auth/logout/` | Invalidate your token | ✓ |
| GET | `/api/auth/me/` | Your own profile | ✓ |
| GET | `/api/users/<username>/` | Public profile | — |
| PATCH | `/api/users/me/update/` | Update bio / avatar | ✓ |
| GET | `/api/users/<username>/posts/` | A user's posts | — |
| GET | `/api/users/<username>/followers/` | Followers list | — |
| GET | `/api/users/<username>/following/` | Following list | — |
| POST/DELETE | `/api/users/<username>/follow/` | Follow / unfollow | ✓ |
| GET | `/api/posts/` | Feed (`?feed=following` to filter) | — |
| POST | `/api/posts/` | Create a post | ✓ |
| GET | `/api/posts/<id>/` | Post detail + comments | — |
| DELETE | `/api/posts/<id>/` | Delete your own post | ✓ |
| POST/DELETE | `/api/posts/<id>/like/` | Like / unlike | ✓ |
| GET/POST | `/api/posts/<id>/comments/` | List / add comments | GET: —, POST: ✓ |
| DELETE | `/api/comments/<id>/` | Delete your own comment | ✓ |

Authenticated requests need an `Authorization: Token <your-token>` header (the frontend handles this automatically once you're logged in — the token is kept in `localStorage`).

## Notes on going further

- `settings.py` uses a dev-only `SECRET_KEY` and `DEBUG = True` — replace both before deploying anywhere public, and load the secret key from an environment variable instead.
- `CORS_ALLOW_ALL_ORIGINS = True` is fine for local development; restrict it to your real frontend origin in production.
- Passwords are hashed by Django's built-in auth system — nothing is ever stored in plain text.
- Image support is URL-based for simplicity (posts/avatars store a URL, not an uploaded file). Adding real file uploads would mean wiring up `Pillow` + DRF's `ImageField` + `multipart/form-data` handling.
