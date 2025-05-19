#!/bin/sh

# Run population if needed
if [ "$POPULATE_DB" = "true" ]; then
  python -m app.db.sample_data
fi

# Start FastAPI
exec fastapi run app --host 0.0.0.0 --port 8000
