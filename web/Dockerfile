FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src .

RUN python manage.py collectstatic --noinput

# ENTRYPOINT [\ 
#     "gunicorn", \
#     "dc_simulate_server.wsgi:application", \
#     "-b", "0.0.0.0:8000"\
# ]