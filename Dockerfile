FROM python:3.11-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY src/app.py .
CMD["python3", "-m", "uvicorn", "main:app", "--reload"]