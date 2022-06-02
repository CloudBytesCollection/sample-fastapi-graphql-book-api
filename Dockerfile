FROM python:3.9.12-slim

# Install Environment Dependencies (Image Base)
RUN pip install fastapi uvicorn poetry wheel virtualenv

EXPOSE 8000

# set working directory
WORKDIR /usr/src/bookapi

# set environment variables
ENV PORT 8000
ENV HOST "0.0.0.0"
ENV DB_URL="mongodb://db:27017"
ENV DB_NAME="bookapi"
ENV PYTHONUNBUFFERED 1

# Copy Required Project Assets
COPY ./src/ /bookapi/src
COPY ./main.py /bookapi
COPY ./pyproject.toml /bookapi

# Change directories
WORKDIR /bookapi

# Install Project Dependencies
RUN poetry config virtualenvs.create false \
  && poetry install

# Entry Point
CMD ["uvicorn", "main:app"]