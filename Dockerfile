FROM python:3.14.7-slim

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 53333

CMD ['python', 'server_echo.py']