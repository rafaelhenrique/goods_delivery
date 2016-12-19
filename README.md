[![Build Status](https://travis-ci.org/rafaelhenrique/goods_delivery.svg?branch=master)](https://travis-ci.org/rafaelhenrique/goods_delivery)

# goods_delivery

API to create maps and return route based on the lowest cost of travel.

## Motivation

This project can be used to reduce complexity of large systems to return better cost and lower path. The base of project is a [NetworkX](https://networkx.github.io/) library which manipulates graphs in Python and implements the Dijkstra's algorithm very easily.

## Installation

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
make run
```

Access url from your favorite browser:

[http://localhost:8000/admin](http://localhost:8000/admin)

Do login (with data specified when you ran createsuperuser) and create an api user and api key.

## Working with API

### Create an map:

Create maps with routes and distances for later reference.

Request using curl:
```
curl -X POST -H "Authorization: Token <your api key here>" \
	-H "Content-Type: application/json" -d '{
    "name": "SP",
    "routes": [
        {"start": "A", "end": "B", "distance": 10},
        {"start": "B", "end": "D", "distance": 15},
        {"start": "A", "end": "C", "distance": 20},
        {"start": "C", "end": "D", "distance": 30},
        {"start": "B", "end": "E", "distance": 50},
        {"start": "D", "end": "E", "distance": 30}
    ]
}' "http://localhost:8000/map"
```

Response example (returns HTTP 201):
```
{
  "id": "1ecef567-2f0f-4ef2-9c78-9e37f55ed560",
  "name": "SP",
  "routes": [
    {
      "start": "D",
      "end": "E",
      "distance": 30
    },
    {
      "start": "B",
      "end": "E",
      "distance": 50
    },
    {
      "start": "C",
      "end": "D",
      "distance": 30
    },
    {
      "start": "A",
      "end": "C",
      "distance": 20
    },
    {
      "start": "B",
      "end": "D",
      "distance": 15
    },
    {
      "start": "A",
      "end": "B",
      "distance": 10
    }
  ]
}
```

### List created maps:

List your maps created.

Request using curl:
```
curl -X GET -H "Authorization: Token <your api key>" \
	-H "Content-Type: application/json" "http://localhost:8000/map"
```

Response example (returns HTTP 200):
```
[
  {
    "id": "1ecef567-2f0f-4ef2-9c78-9e37f55ed560",
    "name": "MG"
  },
  {
    "id": "a3010513-49eb-4d07-979d-89789d738739",
    "name": "SP"
  }
]
```

### Detail of created map:

Detail of your created maps, show routes, id and name of an specific map.

Request using curl:
```
curl -X GET -H "Authorization: Token <your api key>" \
	-H "Content-Type: application/json" \
	"http://localhost:8000/map/<unique id of map>"
```

Response example (returns HTTP 200):
```
{
  "id": "a3010513-49eb-4d07-979d-89789d738739",
  "name": "SP",
  "routes": [
    {
      "start": "D",
      "end": "E",
      "distance": 30
    },
    {
      "start": "B",
      "end": "E",
      "distance": 50
    },
    {
      "start": "C",
      "end": "D",
      "distance": 30
    },
    {
      "start": "A",
      "end": "C",
      "distance": 20
    },
    {
      "start": "B",
      "end": "D",
      "distance": 15
    },
    {
      "start": "A",
      "end": "B",
      "distance": 10
    }
  ]
}
```

*IMPORTANT*: To get unique id of map you need send a get request to list maps or see response of creation of map.

### Show short path:

Based on start, end, autonomy and fuel_price get better route (using [Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra's_algorithm)).

Better route = more cheap and more faster.

Request using curl:
```
curl -X POST -H "Authorization: Token <your api key>" \
	-H "Content-Type: application/json"  -d '{
    "start": "A",
    "end": "D",
    "autonomy": "10.0",
    "fuel_price": "2.5"
}' "http://localhost:8000/map/<unique id of map>/shortpath"
```

Response example (returns HTTP 200):
```
{
  "cost": 6.25,
  "path": [
    "A",
    "B",
    "D"
  ]
}
```

## Response errors examples

### API KEY not provided:

HTTP STATUS CODE: 401 UNAUTHORIZED

Content:
```
{
  "detail": "As credenciais de autenticação não foram fornecidas."
}
```

### Duplicated map name:

HTTP STATUS CODE: 400 BAD REQUEST

Content:
```
{
  "name": [
    "Mapa com este name já existe."
  ]
}
```

### Missing required fields:

HTTP STATUS CODE: 400 BAD REQUEST

Content:
```
{
  "routes": [
    {
      "start": [
        "Este campo é obrigatório."
      ]
    }
} 
```

### Not found map:

HTTP STATUS CODE: 404 NOT FOUND

Without content.

### Value not found:

HTTP STATUS CODE: 400 BAD REQUEST

Content:
```
{
  "start": [
    "start value not found."
  ]
}
```
