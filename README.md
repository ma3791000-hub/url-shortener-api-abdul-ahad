
# URL Shortener API

A local URL Shortener API built with FastAPI, SQLAlchemy, and SQLite.

## Features

- Create short links with automatically generated codes.
- Create links using custom aliases.
- Validate URLs and reject unsupported schemes.
- Redirect short links to their original URLs.
- Handle expired links and unknown codes.
- Track clicks, timestamps, user agents, and referrers.
- View link analytics and top referrers.
- List links with pagination.
- Delete links and their associated click records.
- Store data locally in SQLite.

## Technologies

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic
- SQLite
- Pytest

## Project Structure

```text
URL_Shortener_API/
├── app/
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   ├── main.py
│   ├── database.py
│   └── config.py
├── alembic/
├── data/
├── tests/
├── alembic.ini
├── requirements.txt
└── README.md
```

## Requirements

- Python installed
- Dependencies installed in a virtual environment

## Setup

Open PowerShell in the project directory:

```powershell
cd D:\URL_Shortener_API
```

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Apply database migrations:

```powershell
alembic upgrade head
```

## Run the API

```powershell
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Open the interactive API documentation:

http://127.0.0.1:8000/docs

Health check:

http://127.0.0.1:8000/health

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/links/` | Create a short link |
| GET | `/api/links/` | List links with pagination |
| GET | `/{code}` | Redirect to the original URL |
| GET | `/api/links/{code}/stats` | View link analytics |
| DELETE | `/api/links/{code}` | Delete a link and its click data |

## Run Tests

powershell
python -m pytest -v


Tests use an isolated SQLite database and do not require external network access.

## Configuration

The API is intended to run locally on `127.0.0.1:8000`.

Configuration may include:

- `HOST`
- `PORT`
- `BASE_URL`

The default base URL is:

`http://127.0.0.1:8000`

## Notes

- Only HTTP and HTTPS URLs should be accepted.
- Custom aliases must be unique.
- Expired links return HTTP 410.
- Unknown links return HTTP 404.
- Duplicate aliases return HTTP 409.
- Redirect responses use HTTP 302.

This project is designed for local development and testing.
