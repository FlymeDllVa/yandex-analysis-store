# Yandex – Анализ работы интернет-магазина
> Анализ работы интернет-магазина с помощью PostgreSQL, Redis

[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![DockerBuild](https://img.shields.io/docker/cloud/build/flymedllva/yandex-analysis-store)](https://cloud.docker.com/repository/docker/flymedllva/yandex-analysis-store/general)
[![CodeFactor](https://www.codefactor.io/repository/github/flymedllva/yandex-analysis-store/badge)](https://www.codefactor.io/repository/github/flymedllva/yandex-analysis-store)
[![BCH compliance](https://bettercodehub.com/edge/badge/FlymeDllVa/yandex-analysis-store?branch=master&token=cc4f0aae99176645b88c251b5a93cf41ec2b8a36)](https://bettercodehub.com/)

[Легенда задания](https://github.com/FlymeDllVa/yandex-analysis-store/blob/master/app/static/TASK.pdf)

[English readme](https://github.com/FlymeDllVa/yandex-analysis-store)

<img src="./app/static/images/preview.png" align="center" />

## Технологии
Проект использует следующие технологии:
* [``Docker 19.03.1``](https://github.com/docker) и [``docker-compose 1.24.1``](https://github.com/docker/compose)
    * [``Python 3.7.4``](https://github.com/python) с менеджером зависимостей [``poetry 0.1.0``](https://github.com/sdispater/poetry)
        * Встроенные зависимости
            * re – регулярные выражение для проверки импорта
            * math – для вычисления процентилей
            * datetime – для расчета даты и возраста
            * unittest – тестирование веб-приложения
            * json – помощник по подготовке тестовых данных
            * random – помоощник по подготовке тестовых данных генерирующий псевдослучайные числа
        * Дополнительные зависимости
            * [``Flask 1.1.1``](https://github.com/pallets/flask) – фреймворк для веб-приложений 
            * [``Flask-SQLAlchemy 2.4.0``](https://github.com/pallets/flask-sqlalchemy) – ORM прослока для базы данных
            * [``Flask-RESTful 0.3.7``](https://github.com/flask-restful/flask-restful) – используется для создания RESTful API
            * [``Psycopg2-binary 2.8.3``](https://github.com/psycopg/psycopg2) – драйвер для PostgreSQL
            * [``Redis 3.2.1``](https://github.com/andymccurdy/redis-py) – драйвер для Redis
            * [``Сelery 4.3.0``](https://github.com/celery/celery) – используется для очередей API
    * [``Ngnix 1.17.2``](https://github.com/nginx/nginx) – обратный веб-прокси-сервер
    * [``PostgreSQL 11.4``](https://github.com/postgres/postgres) – Реляционная SQL база данных 
    * [``Redis 5.0.5``](https://github.com/antirez/redis) – NoSQL система управления базами данных

Архитектура проекта:

<img src="./app/static/images/architecture.png" align="center" />

## Тесты

Для тестов используется "Unittest". Тесты запускаются из папки app/tests

Для выполнения тестов требуется работающий сервер. Тесты используют переменные среды Docker и запускаются на сервере

```sh
$ cd app/tests
$ python3 tests.py
```

## Установка

Ubuntu 18.04:

```sh
# Set Time Zome
$ sudo timedatectl set-timezone 'Europe/Moscow' 

# Update the repository and install git
$ sudo apt update && sudo apt upgrade -y
$ sudo apt install git

# Installing Docker
$ sudo apt install apt-transport-https ca-certificates curl software-properties-common
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
$ sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
$ sudo apt update
$ sudo apt install docker-ce

# Installing the "docker" group for the user
$ sudo usermod -aG docker entrant
$ su - entrant

# Installing docker-compose
$ sudo curl -L "https://github.com/docker/compose/releases/download/1.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
$ sudo chmod +x /usr/local/bin/docker-compose

# Copy the repository to the server and navigate to this folder (ask for login and password from git)
$ git clone https://github.com/FlymeDllVa/yandex-analysis-store
$ cd yandex-analysis-store

# Build and run the project
$ docker-compose build
$ docker-compose up -d
$ sudo systemctl enable docker
```

## Автор 

Dmitry Gridnev – flymedllva@gmail.com

@flymedllva – [VK](https://vk.com/flymedllva) – [GitHub](https://github.com/FlymeDllVa)
