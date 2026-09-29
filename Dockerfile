FROM python:3.14-slim AS builder

ENV MALLOC_ARENA_MAX=2

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt


FROM python:3.14-alpine

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.14/dist-packages/ /usr/local/lib/python3.14/dist-packages/

COPY . .

CMD ["python3", "server_echo.py"]
