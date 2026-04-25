FROM python:3.11-slim

ARG PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    SAVE_TEARS_DB_URL=sqlite:////app/data/save_tears.db

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir --index-url "$PIP_INDEX_URL" -r requirements.txt

COPY . .
RUN mkdir -p /app/data

EXPOSE 8000

CMD ["python", "main.py"]
