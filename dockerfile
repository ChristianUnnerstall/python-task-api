FROM python:3.8-alpine

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip --no-cache-dir install -r requirements.txt

COPY ./.env /app/.env
COPY ./app.py /app/app.py

EXPOSE 5000

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]