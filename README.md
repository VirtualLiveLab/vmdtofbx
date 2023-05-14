# dpy-template

template to make [discord.py](https://github.com/Rapptz/discord.py) dev environment with [poetry](https://github.com/python-poetry/poetry) and [pre-commit](https://pre-commit.com).

some useful Github Actions are contained.

you need to setup [pre-commit.ci lite](https://pre-commit.ci/lite.html) to use GitHub Actions fully.

## Installation

clone this repository and run commands below.

installing [poetry](https://github.com/python-poetry/poetry) and [pre-commit](https://pre-commit.com) is needed.

using VSCode is highly recommended.

```bash
  poetry config virtualenvs.in-project true
  poetry install
  pre-commit install
```

## Environment Variables

see [.env.example](https://github.com/sushi-chaaaan/dpy-template/blob/main/.env.example).

you need to set these to `.env` if you want to run bot locally or on Docker.

## Run Locally

set Environment Variables in `.env`.

```bash
  python main.py
```

## Run on Docker with docker-compose

set Environment Variables in `.env`.

```bash
  docker compose up
```

## Deployment

To deploy this project to [Railway](https://railway.app/), just signup and
connect your repository to your Railway project.

You can enable `Check Suites` in deploy settings on Railway
to wait workflow runs before deployment.
