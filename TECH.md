<div align="center">

<img src="client/src/assets/n99_logo.png" alt="n99 Logo" width="240" onerror="this.style.display='none'">
</div>

## Tech Stack

### Frontend
- **Vue 3** - Progressive JavaScript framework
- **Vite** - Next-generation frontend tooling
- **Modern CSS** - Clean, responsive UI

### Backend
- **FastAPI** - High-performance Python web framework
- **Uvicorn** - Lightning-fast ASGI server
- **PostgreSQL** - Robust relational database (via psycopg)
- **Redis** - In-memory data structure store for caching & sessions
- **APScheduler** - Advanced Python Scheduler for background tasks
- **Playwright & Selenium** - Browser automation for web scraping
- **SendInBlue (Brevo)** - Email delivery service

## Project Structure

```
n99/
├── client/              # Vue.js frontend
│   ├── src/
│   │   ├── assets/      # Static assets
│   │   ├── main.js      # Application entry
│   │   └── style.css    # Global styles
│   ├── index.html       # Main HTML template
│   └── package.json     # Frontend dependencies
│
└── server/              # FastAPI backend
    ├── src/
    │   ├── config/      # Application configuration
    │   ├── model/       # Database models
    │   ├── router/      # API routes
    │   ├── services/    # Business logic
    │   │   ├── mail/    # Email templates & service
    │   │   └── scheduler/  # Background job schedulers
    │   └── assets/      # Server assets
    ├── main.py          # Application entry point
    └── requirements.txt # Python dependencies
```

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL
- Redis

### Backend Setup

```bash
cd server
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your database and API credentials

# Start the server
python main.py
```

Server runs at `http://localhost:8000`

### Frontend Setup

```bash
cd client
npm install
npm run dev
```

Client runs at `http://localhost:5173`

## Environment Variables

Create a `.env` file in the `server/` directory:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost/n99

# Redis
REDIS_URL=redis://localhost:6379/0

# Email (SendInBlue/Brevo)
SENDINBLUE_API_KEY=your_api_key_here

# Application
SECRET_KEY=your-secret-key-here
DEBUG=false
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/users` | Create/update user profile |
| `GET` | `/users/{user_id}` | Get user details |
| `POST` | `/tracking` | Start tracking a movie |
| `GET` | `/tracking/{tracking_id}` | Get tracking status |
| `DELETE` | `/tracking/{tracking_id}` | Stop tracking |

## Deployment

The application is designed to run as separate services:

```bash
# Production server
uvicorn server.main:app --host 0.0.0.0 --port 8000 --workers 4

# Production client build
npm run build  # Outputs to dist/
```

Consider using Docker Compose for orchestration:
- Web server (FastAPI)
- Frontend (Nginx)
- PostgreSQL
- Redis
- Worker processes for schedulers