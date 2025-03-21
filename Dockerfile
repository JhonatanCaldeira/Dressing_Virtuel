FROM python:3.10.12

WORKDIR /app
COPY ./ /app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver"]
