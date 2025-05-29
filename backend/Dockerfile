FROM python:3.12.3

RUN apt-get update && apt-get install -y gcc libpq-dev && apt-get clean

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "python wait_for_db.py && uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload"]

