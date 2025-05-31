FROM python:3.11-slim

WORKDIR /app

COPY package.txt .
RUN pip install --no-cache-dir -r package.txt

COPY app.py .

EXPOSE 5001 8001

CMD ["python", "app.py"]
