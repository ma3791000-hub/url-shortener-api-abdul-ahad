# URL Shortener API

A local URL Shortener API built with FastAPI, SQLAlchemy, and SQLite.

## Features

- Create short links with automatically generated codes.
- Create links using custom aliases.
- Add titles to short links.
- Validate HTTP and HTTPS URLs without external network requests.
- Redirect short links to their original URLs.
- Handle expired links and unknown codes.
- Track clicks, timestamps, user agents, and referrers.
- View link analytics, daily clicks, and top referrers.
- List links with pagination.
- Delete links and their associated click records.
- Protect link creation and deletion using API key authentication.
- Store data locally in SQLite.

## Technologies

- Python 3.14
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic
- SQLite
- Pytest
- python-dotenv

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
|   |-- security.py
|
|-- alembic/
|-- data/
|-- tests/
|-- .env.example
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

### 1. Create a virtual environment

```powershell
python -m venv .venv
```

### 2. Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example environment file:

```powershell
Copy-Item .env.example .env
```

Open `.env` and replace the placeholder API key with your own secret key.

The `.env` file contains:

- API_KEY: Secret key used to protect create and delete endpoints.
- HOST: Local server host address.
- PORT: Local server port.
- BASE_URL: Base URL used to generate short links.
- DATABASE_URL: SQLite database connection URL.

Example configuration:

```env
API_KEY=your_secret_api_key_here
HOST=127.0.0.1
PORT=8000
BASE_URL=http://127.0.0.1:8000
DATABASE_URL=sqlite:///./data/app.db
```

**Security:** Never commit your `.env` file or expose your actual API key. Commit `.env.example` instead.

### 5. Create the data directory

```powershell
New-Item -ItemType Directory -Force data
```

### 6. Apply database migrations

```powershell
alembic upgrade head
```

## Run the API

Start the local server using the configured HOST and PORT:

```powershell
python -c "from app.config import HOST, PORT; import uvicorn; uvicorn.run('app.main:app', host=HOST, port=PORT)"
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
| GET | `/{code}` | Redirect to original URL |
| GET | `/api/links/{code}/stats` | View link analytics |
| DELETE | `/api/links/{code}` | Delete a link and click data |

Create and Delete endpoints require the `X-API-Key` header.

## API Usage Examples

Replace `your_secret_api_key_here` with the API_KEY configured in your `.env` file.

### 1. Create a Short Link

```powershell
curl.exe -X POST "http://127.0.0.1:8000/api/links/" `
  -H "Content-Type: application/json" `
  -H "X-API-Key: your_secret_api_key_here" `
  -d '{"url":"https://www.google.com","title":"Google Website"}'
```

### 2. Create a Custom Alias

```powershell
curl.exe -X POST "http://127.0.0.1:8000/api/links/" `
  -H "Content-Type: application/json" `
  -H "X-API-Key: your_secret_api_key_here" `
  -d '{"url":"https://www.google.com","custom_alias":"google1","title":"Google"}'
```

### 3. List Short Links

```powershell
curl.exe "http://127.0.0.1:8000/api/links/?page=1&page_size=10"
```

### 4. View Link Analytics

```powershell
curl.exe "http://127.0.0.1:8000/api/links/google1/stats"
```

### 5. Redirect to Original URL

```powershell
curl.exe -i "http://127.0.0.1:8000/google1"
```

### 6. Delete a Short Link

```powershell
curl.exe -X DELETE "http://127.0.0.1:8000/api/links/google1" `
  -H "X-API-Key: your_secret_api_key_here"
```

## Testing

Run automated tests:

```powershell
python -m pytest -v
```

Tests use an isolated SQLite database and do not require external network access.

The project currently has **16 passing automated tests**.

## Configuration

The application loads environment variables from `.env` using python-dotenv.

| Variable | Description | Default |
|---|---|---|
| API_KEY | API authentication key | Must be configured |
| HOST | Server host | 127.0.0.1 |
| PORT | Server port | 8000 |
| BASE_URL | Short URL base address | http://127.0.0.1:8000 |
| DATABASE_URL | SQLite database URL | Local SQLite database |

## Important Behavior

- Only HTTP and HTTPS URLs are accepted.
- Custom aliases must be unique.
- Expired links return HTTP 410.
- Unknown links return HTTP 404.
- Duplicate aliases return HTTP 409.
- Redirect responses use HTTP 302.
- Missing or incorrect API keys return HTTP 401.
- GET endpoints do not require API key authentication.

## Design Decisions and Trade-offs

- SQLite is used because the application is designed for local development.
- SQLAlchemy manages database operations.
- Alembic manages database schema migrations.
- Short codes are generated using Python's secure random module.
- URL validation checks format and HTTP/HTTPS scheme without making external network requests.
- Click analytics are stored locally in SQLite.
- Tests use an isolated in-memory SQLite database to avoid modifying application data.
- The application runs locally and does not depend on cloud services.

This project is designed for local development and testing.
