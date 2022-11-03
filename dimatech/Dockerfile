FROM python:3.9

ENV PYTHONBUFFERED=1

WORKDIR /app/dimatech

COPY Pipfile Pipfile.lock ./
RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --dev --system --deploy
COPY ./dimatech .

CMD ["python", "__main__.py"]

