ARG ARCH=linux/amd64

FROM --platform=${ARCH} python:3.9

WORKDIR /code

ENV PYTHONPATH "${PYTHONPATH}:/"
ENV PROJECT_NAME=scholarly-api


EXPOSE 80

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]