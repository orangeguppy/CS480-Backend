FROM python:3.11-slim
WORKDIR .
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY auth ./auth
COPY data ./data
COPY models ./models
COPY routers ./routers
COPY main.py ./
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]