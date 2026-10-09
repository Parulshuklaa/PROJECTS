FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python train.py && useradd --create-home appuser && chown -R appuser:appuser /app
USER appuser
ENV PORT=5000
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT} --workers 1 --threads 4 'app:create_app()'"]
