FROM python:3.10-buster as builder

WORKDIR /opt

# python environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONUTF8=1 \
    PYTHONIOENCODING=UTF-8 \
    PIP_DISABLE_PIP_VERSION_CHECK=on

# install python dependencies
COPY requirements.txt /opt/
RUN pip install --no-cache-dir -U pip  &&\
    pip install --no-cache-dir -U setuptools  && \
    pip install --no-cache-dir -U wheel  && \
    pip install --no-cache-dir -r requirements.txt


FROM python:3.10-slim-buster as runner

WORKDIR /app

# permission settings
RUN groupadd -r app && useradd -r -g app app
RUN chown -R app:app /app
USER app

COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --chown=app:app . ./

# start process
ENTRYPOINT ["python", "main.py"]
