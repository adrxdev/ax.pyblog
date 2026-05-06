# Pyblog

A minimal Django blog application with support for posts, categories, comments, and image uploads.

---

## Features

- List all blog posts on the home page
- View individual post details
- Filter posts by category
- Image upload support per post
- Comment display on post detail pages
- Clean black & white UI built with Tailwind CSS

---

## Project Structure

```
ax.pyblog/
├── blog/
│   ├── templates/
│   │   └── blog/
│   │       ├── index.html       # Home — lists all posts
│   │       ├── detail.html      # Single post view
│   │       └── category.html    # Posts filtered by category
│   ├── models.py                # Post, Category, Comments models
│   ├── views.py                 # blog_index, blog_detail, blog_category
│   ├── urls.py                  # URL patterns for blog routes
│   └── apps.py
├── pyblog/
│   ├── settings.py
│   ├── urls.py                  # Root URL config
│   └── wsgi.py
├── static/                      # Static files (if any)
├── media/                       # Uploaded post images
├── db.sqlite3
└── manage.py
```

---

## Setup

### 1. Clone and create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install django pillow
```

### 3. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create a superuser

```bash
python manage.py createsuperuser
```

### 5. Run the development server

```bash
python manage.py runserver
```

Visit `http://localhost:8000` to view the blog and `http://localhost:8000/admin` to manage content.

---

## URL Routes

| URL | View | Description |
|-----|------|-------------|
| `/` | `blog_index` | Lists all posts |
| `/post/<pk>/` | `blog_detail` | Single post detail |
| `/category/<name>/` | `blog_category` | Posts by category |
| `/admin/` | Django Admin | Content management |

---

## Models

### Post
| Field | Type | Description |
|-------|------|-------------|
| `title` | CharField | Post title |
| `body` | TextField | Post content |
| `image` | ImageField | Optional cover image |
| `created_on` | DateTimeField | Auto-set on creation |
| `categories` | ManyToManyField | Linked categories |

### Category
| Field | Type | Description |
|-------|------|-------------|
| `name` | CharField | Category name |

### Comments
| Field | Type | Description |
|-------|------|-------------|
| `author` | CharField | Comment author name |
| `body` | TextField | Comment content |
| `created_on` | DateTimeField | Auto-set on creation |
| `post` | ForeignKey | Linked post |

---

## Settings Reference

```python
# Media files (post images)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Static files
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Templates
TEMPLATES = [{
    'APP_DIRS': True,
    'DIRS': [],
    ...
}]
```

---

## Adding Content

All content is managed through the Django admin panel at `/admin`.

1. Log in with your superuser account
2. Create **Categories** first
3. Create **Posts** — assign categories and optionally upload a cover image
4. Comments are displayed automatically if linked to a post

---

## Tech Stack

- **Backend** — Django 6.x
- **Database** — SQLite (default)
- **Frontend** — Tailwind CSS (CDN)
- **Fonts** — Cormorant Garamond + IBM Plex Mono
- **Image handling** — Pillow
