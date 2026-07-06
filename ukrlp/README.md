# UKRLP Python API Client

Simple Python client for the UKPIMS/UKRLP provider export endpoint:

- `GET /api/providers` (NDJSON stream)
- Authentication via OAuth client-credentials on startup
- APIM subscription key (`Ocp-Apim-Subscription-Key`)
- Configuration from `.env`

## Questions for UKRLP

1. What page size should we use. 1000 sometimes works but I got 500 errors one morning.
1. Pagination
   - What if data changes during requesting pages?
   - Can we request pages asynchronously?
   - Retry strategy for 500s?
1. Rate limits / fair usage
1. Is there a more fleshed out swagger file with responses and example requests etc?
1. What format should datetime inputs be?
1. How are other teams using this API?
   - Any examples in GitHub etc.?

## 1) Install

```bash
python -m venv .venv
. .venv/Scripts/activate
pip install -r requirements.txt
```

## 2) Configure `.env`

Create `.env` from `.env.example` and set values.

Notes:
- On startup the app requests a fresh access token using `OAUTH_TOKEN_URL`, `OAUTH_CLIENT_ID`, `OAUTH_CLIENT_SECRET`, and `OAUTH_SCOPE`.
- These values should be set explicitly in `.env` for the target environment.
- This gateway may reject the default Python `python-requests/*` user agent. The client uses a Postman-compatible user agent by default.

## 3) Run example

```bash
python example_usage.py
```

## 4) Run with Temporal in Docker

This setup uses two containers:

- `temporal` for Temporal server
- `worker` for the UKRLP Temporal worker

### Start services

```bash
docker compose up --build
```

### Trigger a workflow from host

In a second terminal:

```bash
python run_workflow.py
```

This executes `ProviderExportWorkflow` and prints a small provider summary list.

### Stop services

```bash
docker compose down
```

Temporal UI is available on `http://localhost:8233`.

## Filter parameters supported

`stream_providers(...)` supports:

- `updated_since`
- `verified_after`
- `verified_before`
- `ukprn_status`
- `ukprns` (list)
- `page_number`
- `page_size`

Datetime inputs can be Python `datetime` or ISO datetime strings.
