FROM python:3.12-slim

ARG YOUR_ENV

ENV YOUR_ENV=${YOUR_ENV} \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/opt/poetry' \
    POETRY_VERSION=1.8.2

#Install poetry on a global level
RUN apt update
RUN apt install -y curl ffmpeg
RUN curl https://install.python-poetry.org | python3 -

#Copy the poetry.lock and pyproject.toml files to the container
#This way, the dependencies are installed only when the actual requirements change
#and not the code. Speeds up the image build process
COPY poetry.lock pyproject.toml /app/
WORKDIR /app
RUN ls /usr/bin/
# Install the dependencies
RUN ${POETRY_HOME}/bin/poetry install --no-interaction --no-ansi
