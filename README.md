# 🌊 SoundWave - Full-Stack Music Web Application

[![Live Demo](https://img.shields.io/badge/Live_Demo-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://musicclone-yzh4.onrender.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Cloudinary](https://img.shields.io/badge/Cloudinary-Media%20CDN-3448C5?style=for-the-badge&logo=cloudinary&logoColor=white)](https://cloudinary.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

> **SoundWave** is a full-stack music streaming web application built with **Django**, **PostgreSQL**, and **Cloudinary**. It features dynamic audio playback, playlist management, interactive favorites, and a responsive user interface.

🔗 **Live Application:** [https://musicclone-yzh4.onrender.com/](https://musicclone-yzh4.onrender.com/)

---

## ✨ Key Features

- **🎧 Interactive Music Player**:
  - Full playback controls: Play, Pause, Next, Previous, Repeat, and Shuffle.
  - Interactive track progress bar with scrub/seek and volume slider.
- **🔍 Song Exploration & Discovery**:
  - Browse tracks organized by genre, artist, and popularity.
  - Instant search filtering by song title, artist, or genre.
- **❤️ Liked Songs & Favorites**:
  - Authenticated users can like/unlike tracks with instant database persistence.
  - Dedicated personal "Liked Songs" library view.
- **📁 Playlist Management**:
  - Create, customize, and manage personal playlists.
  - Add or remove tracks effortlessly.
- **🔐 User Authentication**:
  - Secure registration, login, logout, and session handling.
- **☁️ Cloud Media Storage**:
  - High-performance album covers and playlist artwork hosted on Cloudinary CDN.
- **🛡️ Django Admin Panel**:
  - Built-in administrator dashboard for managing songs, artists, genres, playlists, and user accounts.
- **🚀 Production-Ready Architecture**:
  - Preconfigured with Gunicorn, WhiteNoise, PostgreSQL database connection pooling (`dj-database-url`), and deployment files (`Procfile`, `build.sh`).

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| **Backend** | Python 3.11, Django 4.2 (MTV Monolithic Architecture) |
| **Frontend** | HTML5, CSS3, JavaScript (Vanilla DOM & Web Audio API) |
| **Database** | SQLite (Development) / PostgreSQL (Production) |
| **Media CDN** | Cloudinary (`django-cloudinary-storage`) |
| **WSGI Server** | Gunicorn |
| **Static Files** | WhiteNoise |
| **Deployment** | Render / Railway |

---

## 📂 Project Structure

```text
SoundWave/
├── Mymusic/                   # Django Project Core Configuration
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py            # Environment settings (DB, Cloudinary, Security)
│   ├── urls.py                # Root URL routing
│   └── wsgi.py                # WSGI entry point for Gunicorn
├── main/                      # Core Music Application
│   ├── migrations/            # Database schema migrations
│   ├── templates/main/        # Application HTML templates
│   ├── admin.py               # Django Admin registration
│   ├── apps.py                # App configuration
│   ├── context_processors.py  # Global context (e.g., user playlists)
│   ├── models.py              # Song, Playlist, and User models
│   ├── tests.py               # Unit tests
│   ├── urls.py                # Main app routes
│   └── views.py               # Views and request handling
├── templates/                 # Global error templates (404, 500)
│   ├── 404.html
│   └── 500.html
├── build.sh                   # Deployment build script
├── Procfile                   # Process file for cloud hosting
├── requirements.txt           # Project dependencies
├── data.json                  # Seed data (songs, playlists, demo data)
├── upload_media.py            # Cloudinary media synchronization script
└── manage.py                  # Django CLI utility
```

---

## 🚀 Getting Started (Local Development)

### 1. Prerequisites
- Python 3.10 or 3.11 installed
- Git installed

### 2. Clone the Repository
```bash
git clone https://github.com/TunganaVinodKumar/SoundWave.git
cd SoundWave
```

### 3. Create & Activate a Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables
Create a `.env` file or export the following variables:

```env
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

# Cloudinary Credentials (Optional for local development)
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

### 6. Run Migrations & Load Data
```bash
# Run database migrations
python manage.py migrate

# Load initial songs and playlists
python manage.py loaddata data.json
```

### 7. Run the Development Server
```bash
python manage.py runserver
```
Open **`http://127.0.0.1:8000/`** in your browser to view the application.

---

## 🌐 Production Deployment (Render / Railway)

### Environment Variables

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string |
| `DJANGO_SECRET_KEY` | Secure secret key for Django |
| `DJANGO_DEBUG` | Set to `False` in production |
| `DJANGO_ALLOWED_HOSTS` | `.onrender.com,.railway.app,localhost` (or `*`) |
| `CLOUDINARY_CLOUD_NAME` | Cloudinary account name |
| `CLOUDINARY_API_KEY` | Cloudinary API key |
| `CLOUDINARY_API_SECRET` | Cloudinary API secret |
| `PYTHON_VERSION` | `3.11.9` |

### Deployment Commands
- **Build Command**:
  ```bash
  python manage.py collectstatic --no-input && python manage.py migrate && python manage.py loaddata data.json
  ```
- **Start Command**:
  ```bash
  gunicorn Mymusic.wsgi:application --bind 0.0.0.0:$PORT
  ```

---

## 👤 Author

**Tungana Vinod Kumar**
- GitHub: [@TunganaVinodKumar](https://github.com/TunganaVinodKumar)
- Repository: [TunganaVinodKumar/SoundWave](https://github.com/TunganaVinodKumar/SoundWave)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
