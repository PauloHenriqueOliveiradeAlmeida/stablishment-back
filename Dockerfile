FROM python:3.13-alpine AS runtime

WORKDIR /app

COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt
COPY  . /app

RUN apk add --no-cache libffi-dev=3.4.7-r0 gcc=14.2.0-r4 musl-dev=1.2.5-r9

EXPOSE 3000

CMD ["fastapi", "run", "--host", "0.0.0.0", "--port", "3000"]

