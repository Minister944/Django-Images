# Django-Images

This project is a web application for storing and sharing images. It allows users to upload images, view other images and create thumbnails. The application provides user authentication and controls access to images according to permissions.

## Installation

```bash
poetry shell
poetry install
```

## Run the app

```bash
cd api
python manage.py runserver
```

## Run the tests

```bash
python manage.py test
```

## REST API

`GET /api/login`

`GET /api/me`

`POST /api/upload`

`GET /api/image/{id_image}/{resolution}`
