FROM python:3.9.18-slim-bullseye

RUN pip3 install --no-cache-dir \
    Django==4.2.9 \
    psycopg2-binary==2.9.9 \
    gunicorn==21.2.0 \
    uvicorn==0.27.1 && \
    useradd -m -d /app -s /bin/bash app


WORKDIR /app
USER app
COPY ./backend /app

CMD ["python3", "-u", "manage.py", "runserver", "0.0.0.0:8000"]