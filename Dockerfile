FROM python:3.10 

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt -vvv

COPY . .

RUN python manage.py collectstatic --noinput
RUN python -m pip install pillow
RUN apt-get update && apt-get install -y poppler-utils


CMD ["python", "manage.py", "migrate"]
