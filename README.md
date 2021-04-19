#A URL Shortener RESTful Application Using Docker
URL shortening is a technique on the World Wide Web in which a Uniform Resource Locator (URL) may be made substantially shorter and still direct to the required page. This is achieved by using a redirect which links to the web page that has a long URL.

## Description
This app wrote on the Django framework which is powered by celery, redis, rabbitmq, postgresql, docker and DRF. The usage of each item describe as follow:
```textmate
celery: To increment visit count async in the background and decrease redirect time.The celery could run on the another server and using a clustered DB.
postgresql: using as Database of the product.
rabbitmq: Using as celery broker.
redis: Using to fast get the original url from short URL (in memory cache).
docker: Used for containerize the project for better deploy experience.
DRF: Used for publish best practice of REST api.
```
## Project's tree
```text
.
├── apps
│   ├── core
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   └── views.py
│   ├── redirect
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── permissions.py
│   │   ├── serializers.py
│   │   ├── tasks.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   ├── utils.py
│   │   └── views.py
│   └── shortener
│       ├── admin.py
│       ├── apps.py
│       ├── __init__.py
│       ├── models.py
│       ├── permissions.py
│       ├── serializers.py
│       ├── tasks.py
│       ├── tests.py
│       ├── urls.py
│       ├── utils.py
│       └── views.py
├── docker-compose.yml
├── Dockerfile
├── dockerize_conf
│   ├── django_entry_point.sh
│   ├── nginx
│   │   ├── django.conf
│   │   ├── Dockerfile
│   │   └── nginx.conf
│   ├── uwsgi.ini
│   └── uwsgi_params
├── manage.py
├── media
├── README.md
├── requirements.txt
├── static ...
├── swagger.yaml
├── URLShortener
│   ├── asgi.py
│   ├── celery.py
│   ├── __init__.py
│   ├── redis.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── utils.py

```
#### Short url algorithm
A Better Solution is to use the integer id stored in the database and convert the integer to a character string that is at most 6 characters long. This problem can basically seen as a base conversion problem where we have a 10 digit input number and we want to convert it into a 6 character long string.
Below is one important observation about possible characters in URL.
A URL character can be one of the following
1) A lower case alphabet [‘a’ to ‘z’], total 26 characters
2) An upper case alphabet [‘A’ to ‘Z’], total 26 characters
3) A digit [‘0’ to ‘9’], total 10 characters

There are total 26 + 26 + 10 = 62 possible characters.

So the algorithm is to convert a decimal number to base 62 number.

To get the original long URL, we need to get URL id in the database. The id can be obtained using base 62 to decimal conversion. Please note first we are try to get the original URL from redis using short_url as key without any hit to RDBMS and although increment the visist count async using Celery in the background.
Some benefit of this algorithm are:
1) Not need to hit to DB rather than using random string (checking if random string is unique or not need more hit DB).
2) It is possible to get back to the original url from short link very fast and secure.
3) supporting big range of submitting new URL without any worry.
4) Fast achieve to original url from short link.
## Dependency
```text
docker
docker-compose
```
### Dependency installation

Quick and easy install script provided by Docker:

```shell script
curl -sSL https://get.docker.com/ | sh
```
To install docker-compose on Debian base OS:
```shell script
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

```
If you're not willing to run a random shell script, please see the [installation](https://docs.docker.com/engine/installation/linux/) instructions for your distribution.

If you are a complete Docker newbie, you should follow the [series of tutorials](https://docs.docker.com/engine/getstarted/) now.

## Test
go to project's root directory and use following commands:
```shell script
cd apps
./manage.py test
```

## Run
clone the git repository and got to project's root directory in the terminnal and run following command:
```shell script
sudo docker-compose up --build -d
```
Then it is possible to go to following url from your browser to start create short_url:
http://localhost:80/api/v1/url_shortener/

## Swagger file
Please refer to swagger file in the root of the project for more information about API.

## Postman collection
it is possible to use postman collection to using application too.
[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/843b8733730cd0465fc0#?env%5Burl%20shortener%5D=W3sia2V5IjoiZG9tYWluIiwidmFsdWUiOiJodHRwOi8vbG9jYWxob3N0OjgwMDAiLCJlbmFibGVkIjp0cnVlfV0=)

## Licence
Licence by Myself :)
Please feel free to send me email Mortaz.Mehdi@gmail.com