# datatrans-api-python-types

Generate Python types for data types used in the Datatrans OpenAPI specification.

## Development Setup

```
python3 -m venv venv
venv/bin/pip install -e '.[dev]'
```

## Running

```
venv/bin/datatrans-api-python-types datatrans-openapi-specification-2.0.32.json > api.py
```
