FROM python:3.12.10-slim-bookworm

WORKDIR /frontend

COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./images ./images

COPY ./src ./src

EXPOSE 8501

CMD [ "streamlit", "run", "src/Hotel.py" ]
