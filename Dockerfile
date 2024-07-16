FROM python:3.11-alpine

ARG APP_HOME=/backend

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN mkdir ${APP_HOME}
WORKDIR ${APP_HOME}

# 빌드 도구 및 라이브러리 설치
RUN apk update && apk add --no-cache \
    build-base \
    libffi-dev \
    openssl-dev \
    python3-dev \
    py3-setuptools \
    && rm -rf /var/cache/apk/*

# install requirements
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# copy all
COPY . ${APP_HOME}

# copy start script & run
COPY ./script/start /start
RUN sed -i  's/\r$//g' /start
RUN chmod +x /start

# copy start script & run
COPY ./script/start /start
RUN sed -i  's/\r$//g' /start
RUN chmod +x /start

# copy start entrypoint & run
COPY ./script/entrypoint /entrypoint
RUN sed -i  's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

ENTRYPOINT [ "/entrypoint" ]

CMD [ "/start" ]