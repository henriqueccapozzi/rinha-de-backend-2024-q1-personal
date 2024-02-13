FROM python:3.9.18-slim-bullseye

RUN apt-get update && \
    apt-get install -y gcc python3-dev libev-dev && \
    pip3 install --no-cache-dir \
    Django==4.2.9 \
    psycopg2-binary==2.9.9 \
    gunicorn==21.2.0 \
    bjoern==3.2.2 && \
    useradd -m -d /app -s /bin/bash app


WORKDIR /app
USER app
COPY ./backend /app

CMD ["python3", "-u", "manage.py", "runserver", "0.0.0.0:8000"]