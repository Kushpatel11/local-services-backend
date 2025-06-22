FROM python:3.11-slim

WORKDIR /URBANEASE-BACKEND/local-services-backend

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .
COPY .env .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=8000"]