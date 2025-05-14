FROM python:3.13.3-alpine AS builder
WORKDIR /app
RUN apk add --no-cache build-base
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.13.3-alpine
WORKDIR /app
COPY --from=builder /install /usr/local
COPY . .
CMD ["python3", "main.py"]