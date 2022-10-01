ARG ARCH=linux/amd64

FROM --platform=${ARCH} python:3.9

WORKDIR /code

ENV PYTHONPATH "${PYTHONPATH}:/"
ENV PORT=80
ENV SCHOLARLY_PROJECT_NAME=scholarly-api
ENV SCHOLARLY_BACKEND_CORS_ORIGINS=
ENV SCHOLARLY_SCRAPER_API_KEY=
ENV CONNECTION_METHOD=freeproxy

EXPOSE 80

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:80"]