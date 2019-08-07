FROM python:3.7.4

ENV TZ=Europe/Moscow

RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

ENV PATH ~/.poetry/bin:$PATH

ADD ./pyproject.toml .

RUN ~/.poetry/bin/poetry config settings.virtualenvs.create false \
    && ~/.poetry/bin/poetry install  --no-interaction --no-ansi
