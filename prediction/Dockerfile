FROM python:3.11.5-slim

WORKDIR /app

COPY . /app
RUN pip install --upgrade pip
RUN pip install --default-timeout=1000 --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "prediction.py"]