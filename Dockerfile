# ---------------------------------------------
# Base Stage: Install Poetry and System Setup
# ---------------------------------------------
FROM python:3.10-alpine AS base

# Setting up work directory
WORKDIR /home/app
ENV PATH="/root/.local/bin:${PATH}"

RUN apk add --no-cache --virtual .build-deps gcc musl-dev geos-dev geos

COPY pyproject.toml poetry.lock ./
COPY README.md ./

RUN pip3 install --user poetry==1.8.5

# ---------------------------------------------
# Build Stage: Install All Dependencies, Build the Package
# ---------------------------------------------
FROM base AS builder

WORKDIR /home/app

# Copying the source code
COPY reporter_lib ./reporter_lib

# Install only production dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --without dev,test --no-interaction --no-ansi

# Building the package (this will create the dist/ folder and requirements.txt)
RUN poetry build
RUN poetry export --without dev,test --without-hashes -f requirements.txt > requirements.txt

# ---------------------------------------------
# Development Stage: Install Dev Dependencies
# ---------------------------------------------
FROM base AS development

RUN apk add make

WORKDIR /home/app

# Install all dependencies including dev and test
RUN poetry config virtualenvs.create false \
    && poetry install --with dev,test --no-interaction --no-ansi

# Copy the entire project
COPY . .

# Expose dev environment variables
ENV PYTHONUNBUFFERED=1