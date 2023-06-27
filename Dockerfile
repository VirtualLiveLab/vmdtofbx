ARG PYTHON_VERSION_CODE=3.11

FROM python:${PYTHON_VERSION_CODE}-buster as builder
ARG PYTHON_VERSION_CODE
WORKDIR /opt
# python environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# install python dependencies
COPY requirements.txt /opt/
RUN python -m pip install --no-cache-dir -U pip setuptools wheel && \
    python -m pip install --no-cache-dir -r requirements.txt

FROM python:${PYTHON_VERSION_CODE}-slim-buster as runner
ARG PYTHON_VERSION_CODE
WORKDIR /app
# permission settings
RUN groupadd -r app && useradd -r -g app app
RUN chown -R app:app /app
USER app

COPY --from=builder /usr/local/lib/python${PYTHON_VERSION_CODE}/site-packages /usr/local/lib/python${PYTHON_VERSION_CODE}/site-packages
COPY --chown=app:app . ./

# start process
ENTRYPOINT ["python", "main.py"]
