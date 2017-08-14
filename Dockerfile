FROM jfloff/alpine-python

ENV API_SERVER_HOME=/opt/www
WORKDIR $API_SERVER_HOME

RUN apk update \
    && apk add --no-cache --virtual=.build_dependencies build-base libffi-dev \
    && apk del .build_dependencies

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt \
    && rm -rf ~/.cache/pip

COPY . .

CMD [ 'gunicorn -c gunicorn.py --reload "app:create_app()"' ]
