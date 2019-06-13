# Flask RESTful API

API is responsible for converting the data containing the price for fruits based on country, city and currency. 

The application takes JSON array containing following keys:
`country`
`city`
`fruit`
`currency`
`price`

The data is saved into database and can be retrieved using specifics API endpoints.

The purpose of the project was to learn how to create a Flask API, which has CRUD operations and can interact with the database.

## Setup
```buildoutcfg
docker build -t <name> <dockerfile directory>
docker run -p 5000:5000 -it -t <name>
```

## Endpoints

GET, POST
```
/api/v1/fruits
```
GET, PUT, DELETE
```buildoutcfg
/api/v1/fruit/<id>
```
GET
```
/api/v1/fruit/nest?key=<key-name>
```

## Example of usage

In order to send a JSON data use endpoint `/api/v1/fruits` with `POST` request and add into the body of the request following data:

```
[
   {
    "country": "US",
    "city": "Clevland",
    "fruit": "apple",
    "currency": "GBP",
    "price": 1.1
  },
  {
    "country": "RU",
    "city": "Moscaw",
    "fruit": "banana",
    "currency": "FBP",
    "price": 5.5
  }
]
```

Example:

![fruits-post-request](https://user-images.githubusercontent.com/32844693/59459996-56ec4a80-8e1e-11e9-8682-9eed151f2f0e.PNG)

In order to get all JSON data use endpoint `/api/v1/fruits` with `GET` request.

Example:

![fruits-get-request](https://user-images.githubusercontent.com/32844693/59461134-f7436e80-8e20-11e9-9698-a7100a1ec7c9.PNG)

In order to get a single row use endpoint `/api/v1/fruit/<id>` with `GET` request.

In order to delete a single row use endpoint `/api/v1/fruit/<id>` with `DELETE` request.

In order to update a single row use endpoint `/api/v1/fruit/<id>` with `PUT` request and add into the body of the request following data:

```buildoutcfg
{
    "country": "FR",
    "city": "Lyon",
    "fruit": "orange",
    "currency": "EUR",
    "price": 2
}
```

Example:

![fruit-put-request](https://user-images.githubusercontent.com/32844693/59459762-de858980-8e1d-11e9-95bd-b1489d349b2d.PNG)

In order to get nested dictionaries based on provided keys use endpoint `/api/v1/fruit/nest?key=<key-name>` with `GET` request.
<br/>
In the request specify keys, which will be nested. Not specified keys will be store in the array of the last dictionary.

Example:

![nest-get-1](https://user-images.githubusercontent.com/32844693/59461899-c7956600-8e22-11e9-83ad-c6eaf53ae2d3.PNG)

![nest-get-2](https://user-images.githubusercontent.com/32844693/59461904-c95f2980-8e22-11e9-9df2-d03ca9cd712a.PNG)

## Technologies

* Python 3.7.0
* Flask 1.0.3
* Flask-RESTful 0.3.7
* SQLAlchemy 1.3.4
* Docker