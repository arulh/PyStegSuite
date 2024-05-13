FROM python:3.12

WORKDIR /app

COPY app/app.py /app
COPY docs/requirements.txt /app

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "app.py"]
