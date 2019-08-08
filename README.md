# Yandex – Analysis of the online store
> Analysis of online store using PostgreSQL, Redis 

[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![DockerBuild](https://img.shields.io/docker/cloud/build/flymedllva/yandex-analysis-store)](https://cloud.docker.com/repository/docker/flymedllva/yandex-analysis-store/general)
[![CodeFactor](https://www.codefactor.io/repository/github/flymedllva/yandex-analysis-store/badge)](https://www.codefactor.io/repository/github/flymedllva/yandex-analysis-store)
[![BCH compliance](https://bettercodehub.com/edge/badge/FlymeDllVa/yandex-analysis-store?branch=master&token=cc4f0aae99176645b88c251b5a93cf41ec2b8a36)](https://bettercodehub.com/)

[The legend of the task](https://github.com/FlymeDllVa/yandex-analysis-store/blob/master/app/static/TASK.pdf)

[Russian readme](https://github.com/FlymeDllVa/yandex-analysis-store/blob/master/README_RU.md)

<img src="https://raw.githubusercontent.com/FlymeDllVa/yandex-analysis-store/master/app/static/images/preview.png?token=AH5ZRU72R47B5VOFSCUQRCS5KWHTC" align="center" />

## Technologies
Project is created with:
* [``Docker 19.03.1``](https://github.com/docker) and [``docker-compose 1.24.1``](https://github.com/docker/compose)
    * [``Python 3.7.4``](https://github.com/python) with [``poetry 0.1.0``](https://github.com/sdispater/poetry) dependency Manager
        * Built-in dependencies
            * re – regular expression to validate the import
            * math – to calculate percentiles
            * datetime – to calculate date and age
            * unittest – to test a web application
            * json – assistant for the preparation of test data
            * random – assistant for unittest in the preparation of pseudo-random
        * Third party dependencies
            * [``Flask 1.1.1``](https://github.com/pallets/flask) – web application framework
            * [``Flask-SQLAlchemy 2.4.0``](https://github.com/pallets/flask-sqlalchemy) – ORM layer for database
            * [``Flask-RESTful 0.3.7``](https://github.com/flask-restful/flask-restful) – used for create RESTful API
            * [``Psycopg2-binary 2.8.3``](https://github.com/psycopg/psycopg2) – driver for PostgreSQL
            * [``Redis 3.2.1``](https://github.com/andymccurdy/redis-py) – driver for Redis
            * [``Сelery 4.3.0``](https://github.com/celery/celery) – used for API queues
    * [``Ngnix 1.17.2``](https://github.com/nginx/nginx) – web proxy server
    * [``PostgreSQL 11.4``](https://github.com/postgres/postgres) – SQL relational database
    * [``Redis 5.0.5``](https://github.com/antirez/redis) – NoSQL database management system

The architecture of the project:

<img src="https://raw.githubusercontent.com/FlymeDllVa/yandex-analysis-store/master/app/static/images/architecture.png?token=AH5ZRUYSJYUYTPUUNJCIMBC5KWHTY" align="center" />

## Tests

To run the tests, use "Unittest". Tests are run from the app/tests folder

A running server is required to run the tests. Tests are used by environment Docker

```sh
$ cd app/tests
$ python3 tests.py
```

## Installation

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

## Author 

Dmitry Gridnev – flymedllva@gmail.com

@flymedllva – [VK](https://vk.com/flymedllva) – [GitHub](https://github.com/FlymeDllVa)

