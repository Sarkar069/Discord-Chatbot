FROM python:3.13.3-alpine AS builder
WORKDIR /app
RUN apk add --no-cache build-base libffi-dev openssl-dev
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.13.3-alpine
WORKDIR /app
RUN apk add --no-cache libffi openssl
COPY --from=builder /install /usr/local
COPY . .
CMD ["python3", "-u", "main.py"]
