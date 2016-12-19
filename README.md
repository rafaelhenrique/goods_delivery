[![Build Status](https://travis-ci.org/rafaelhenrique/goods_delivery.svg?branch=master)](https://travis-ci.org/rafaelhenrique/goods_delivery)

# goods_delivery

API to return route based on the lowest cost of travel.

## Instalation

Clone this project:

```
git clone https://github.com/rafaelhenrique/goods_delivery.git
```

Enter on directory:

```
cd goods_delivery
```

Create virtualenv:

```
python3.5 -m venv .venv
```

Activate your virtualenv:

```
source .venv/bin/activate
```

Copy localenv file example to root directory of this project:

```
cp contrib/localenv .env
```

Now configure your .env file (use your preferred text editor), then run installation:

```
make install
```

## Run project for development

```
make run
```

## More commands/target on make

```
make help
```

## How i use API?

You need to create a superuser first:

```
make createsuperuser
```

Now access url from your favorite browser:

[http://localhost:8000/admin](http://localhost:8000/admin)

Do login (with data specified when you ran createsuperuser) and create an api user and api key.

