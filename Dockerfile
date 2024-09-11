ARG ARCH=linux/amd64
#ARG ARCH=linux/arm64/v8

FROM --platform=${ARCH} python:3.9

WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app

EXPOSE 80

CMD ["fastapi", "run", "app/main.py", "--port", "80"]
