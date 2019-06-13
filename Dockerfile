FROM python:3.7

WORKDIR /app

ENV PYTHONUNBUFFERED 1

COPY Pipfile* /app/

RUN pip install pipenv && pipenv install --system

# Install python packages
RUN pipenv install --deploy --system

# Install service
COPY . .

CMD python src runserver 0.0.0.0:8000
