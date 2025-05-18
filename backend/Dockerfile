FROM python:3.12.10-slim-bookworm

WORKDIR /backend

COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

EXPOSE 8000

CMD ["fastapi", "run", "app", "--host", "0.0.0.0", "--port", "8000"]
