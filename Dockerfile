FROM python:3.10

RUN apt-get update && apt-get install -y build-essential

RUN pip install --upgrade pip

COPY . /app

RUN rm /app/db.sqlite3

WORKDIR /app

RUN pip install -r requirements.txt

RUN python3 manage.py makemigrations
RUN python3 manage.py migrate   

EXPOSE 8000

CMD ["scripts/entrypoint.sh"]
