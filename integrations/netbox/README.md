# NetBox Integration Client

Python-based reusable NetBox integration client for inventory automation and Source of Truth operations.

Supports:
- Raw REST API requests
- Pynetbox SDK integration
- Pagination handling
- Generic filtering
- Logging
- Environment variable support

---

# Features

## Requests-based API Access
- Generic GET requests
- Handles paginated responses
- Read-only token support
- Timeout handling
- Logging support

## Pynetbox SDK Support
- Dynamic API path handling
- Filtering support
- Generic reusable methods

---

# Project Structure

```text
integrations/
└── netbox/
    ├── client.py
    └── __init__.py
```

---

# Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create `.env`

```env
NETBOX_URL=http://netbox.local
NETBOX_V1_TOKEN_RO=xxxxxxxx
NETBOX_V1_TOKEN_RW=xxxxxxxx
NETBOX_V2_TOKEN_RO=xxxxxxxx
NETBOX_V2_TOKEN_RW=xxxxxxxx
```

---

# Usage

## Requests API Example

```python
from integrations.netbox.client import NetBoxClient

result = NetBoxClient.get_requests(
    url='/api/dcim/sites/'
)

print(result)
```

---

## Pynetbox Example

### Get All Sites

```python
result = NetBoxClient.get_pynetbox(
    api='dcim',
    sub_api='sites'
)
```

### Filter Devices

```python
result = NetBoxClient.get_pynetbox(
    api='dcim',
    sub_api='devices',
    site='hyd-site-01'
)
```

---

# Logging

Logs are stored in:

```text
logs/integrations/netbox.log
```

---

# Future Improvements

Planned:
- POST support
- PATCH support
- DELETE support
- Retry mechanism
- Session reuse
- Async support
- Custom exceptions
- Pydantic models
- Data validation

---

# Author

B S DADA KHALANDAR
Network SPECIALIST