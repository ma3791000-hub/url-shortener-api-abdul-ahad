# URL Shortener API

A local URL Shortener API built with FastAPI, SQLAlchemy, and SQLite.

## Features

- Create short links with automatically generated codes.
- Create links using custom aliases.
- Validate URLs and reject unsupported schemes.
- Redirect short links to their original URLs.
- Handle expired links and unknown codes.
- Track clicks, timestamps, user agents, and referrers.
- View link analytics, daily clicks, and top referrers.
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
|
|-- app/
|   |-- models/
|   |-- routers/
|   |-- schemas/
|   |-- services/
|   |-- main.py
|   |-- database.py
|   |-- config.py
|
|-- alembic/
|-- data/
|-- tests/
|-- offline_packages/
|-- alembic.ini
|-- requirements.txt
|-- README.md
```

## Requirements

- Python 3.14
- Dependencies listed in requirements.txt
- A virtual environment

## Setup

Open PowerShell in the project directory:

```powershell
cd D:\URL_Shortener_API
```

Create a virtual environment:

```powershell
python -m venv .venv
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

## Offline Installation

The project includes an `offline_packages` folder containing the downloaded dependency packages.

To install dependencies without accessing the online package index:

```powershell
python -m pip install --no-index --find-links=offline_packages -r requirements.txt
```

The included package files are intended for the tested Windows and Python 3.14 environment.

## Run the API

Start the local server:

```powershell
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Interactive API documentation:

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

## API Usage Examples

### 1. Create a Short Link

```powershell
curl.exe -X POST "http://127.0.0.1:8000/api/links/" `
  -H "Content-Type: application/json" `
  -d '{"url":"https://www.google.com"}'


```powershell
curl.exe -X DELETE "http://127.0.0.1:8000/api/links/google1"

```powershell
curl.exe "http://127.0.0.1:8000/api/links/?page=1&page_size=10"

```powershell
curl.exe "http://127.0.0.1:8000/api/links/google1/stats"

```powershell
curl.exe -i "http://127.0.0.1:8000/google1"

```powershell
curl.exe -X POST "http://127.0.0.1:8000/api/links/" `
  -H "Content-Type: application/json" `
  -d '{"url":"https://www.google.com","custom_alias":"google1"}'

Run the following command from the project directory:

```powershell
python -m pytest -v
```

Tests use an isolated SQLite database and do not require external network access.

The project has been tested with 12 passing automated tests.

## Configuration

The API runs locally by default at `127.0.0.1:8000`.

The following environment variables can be used to configure the application:

- `HOST`: Host address. Default: `127.0.0.1`
- `PORT`: Port number. Default: `8000`
- `BASE_URL`: Base URL for generated short links. Default: `http://127.0.0.1:8000`

Example PowerShell commands:

```powershell
$env:HOST = "127.0.0.1"
$env:PORT = "8000"
$env:BASE_URL = "http://127.0.0.1:8000"


Set these variables before starting the API.

- Only HTTP and HTTPS URLs should be accepted.
- Custom aliases must be unique.
- Expired links return HTTP 410.
- Unknown links return HTTP 404.
- Duplicate aliases return HTTP 409.
- Redirect responses use HTTP 302.

This project is designed for local development and testing.

## Design Decisions and Trade-offs

- SQLite is used because the application is designed for local development and does not require an external database server.
- SQLAlchemy is used to manage database operations and keep database code organized.
- Alembic is used for database schema migrations.
- Short codes are generated using Python's secure random module to reduce the chance of collisions.
- URL validation checks the URL format and HTTP/HTTPS scheme without making external network requests.
- Click analytics are stored in SQLite, which keeps the application simple but may not be suitable for very high traffic.
- Tests use an isolated in-memory SQLite database to avoid modifying the actual application database.
- The application runs on localhost by default and does not depend on cloud services.