# AI Customer Support

A small customer support ticketing system with AI-assisted ticket triage. Support agents can manage customers and tickets through a REST API and a Streamlit dashboard, and use a locally-hosted LLM (via [Ollama](https://ollama.com)) to summarize tickets, gauge sentiment, and draft replies.

## Features

- **Customer management** — create, read, update, and delete customer records
- **Ticket management** — create, read, update, and delete support tickets, linked to customers
- **AI ticket tools**, powered by a local Llama 3 model:
  - Summarize a ticket in 1–2 sentences
  - Analyze sentiment (Positive / Neutral / Negative + reasoning)
  - Draft a suggested reply
- **Streamlit dashboard** for adding customers/tickets and running AI analysis without touching the API directly
- **File logging** of application activity to `logs/app.log`

## Tech Stack

| Layer     | Technology |
|-----------|------------|
| Backend   | FastAPI, SQLAlchemy, Pydantic |
| Database  | SQLite (`support.db`) |
| AI        | [Ollama](https://ollama.com) running the `llama3` model, called over its local HTTP API |
| Frontend  | Streamlit |
| Logging   | Python `logging` module |

## Project Structure

```
AI Customer Support/
├── app/
│   ├── main.py          # FastAPI app setup, router registration, CORS
│   ├── database.py      # SQLAlchemy engine/session config (SQLite)
│   ├── models.py        # ORM models: Customer, Ticket, Response
│   ├── schemas.py       # Pydantic request/response schemas
│   ├── crud.py          # Database access functions
│   ├── ai.py            # Ollama integration (summarize / sentiment / reply)
│   ├── routes/
│   │   ├── customers.py # /customers endpoints
│   │   ├── tickets.py   # /tickets endpoints
│   │   └── ai_tools.py  # /ai-tools endpoints
│   └── utils/
│       └── logger.py    # Logging setup
├── frontend/
│   └── stream.py         # Streamlit dashboard
├── logs/                  # App log output (created at runtime)
├── test_ai.py             # Manual smoke test script for the AI endpoints
├── support.db             # SQLite database file
└── requirements.txt
```

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com) installed and running locally, with the `llama3` model pulled:
  ```bash
  ollama pull llama3
  ollama serve
  ```
  The backend expects Ollama's API at `http://localhost:11434`.

## Setup

1. **Install dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Start Ollama** (in its own terminal, if not already running)
   ```bash
   ollama serve
   ```

3. **Start the backend API**
   ```bash
   python -m uvicorn app.main:app --reload
   ```
   - API base: `http://localhost:8000`
   - Interactive docs: `http://localhost:8000/docs`
   - The SQLite tables are created automatically on startup.

4. **Start the frontend dashboard** (in a separate terminal)
   ```bash
   streamlit run frontend/stream.py
   ```
   - Dashboard: `http://localhost:8501`

## API Reference

### Customers — `/customers`
| Method | Path | Description |
|--------|------|-------------|
| POST   | `/` | Create a customer |
| GET    | `/` | List customers (`skip`, `limit` query params) |
| GET    | `/{customer_id}` | Get a single customer |
| PUT    | `/{customer_id}` | Update a customer |
| DELETE | `/{customer_id}` | Delete a customer |

### Tickets — `/tickets`
| Method | Path | Description |
|--------|------|-------------|
| POST   | `/` | Create a ticket (validates that `customer_id` exists) |
| GET    | `/` | List tickets (`skip`, `limit` query params) |
| GET    | `/{ticket_id}` | Get a single ticket |
| PUT    | `/{ticket_id}` | Update a ticket |
| DELETE | `/{ticket_id}` | Delete a ticket |

### AI Tools — `/ai-tools`
| Method | Path | Description |
|--------|------|-------------|
| POST | `/summarize-ticket/{ticket_id}` | Returns a short summary of the ticket message |
| POST | `/analyze-sentiment/{ticket_id}` | Returns sentiment + reasoning for the ticket message |
| POST | `/suggest-reply/{ticket_id}` | Returns a drafted support reply |

All three fetch the ticket by ID (404 if not found) and pass its `message` to the local LLM. Responses can take a while since generation runs on-machine (client timeout is set to 300s).

## Data Model

- **Customer**: `id`, `name`, `email` → has many Tickets
- **Ticket**: `id`, `customer_id`, `subject`, `message`, `status` (default `"open"`), `created_at` → has many Responses
- **Response**: `id`, `ticket_id`, `response_text`, `created_at`

## Testing

`test_ai.py` is a manual smoke-test script (not a pytest suite). With the backend running, it creates a customer, creates a ticket, and calls the summarize endpoint:

```bash
python test_ai.py
```

## Known Limitations / Next Steps

- The `Response` model, schema, and CRUD functions exist, but there's no `/responses` route yet — AI-generated output isn't currently saved back to the database.
- CORS is locked to `http://localhost:8501` in `app/main.py`; update this if you host the frontend elsewhere.
- No authentication/authorization on any endpoint.
- `requirements.txt` shipped empty in this project — it's been populated based on the actual imports; double-check versions before deploying.
 
