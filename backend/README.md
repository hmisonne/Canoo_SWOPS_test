# API Reference

We are using a json file to mock the system that controls thermostat and lights `data.json`.

## Error Handling
Errors are returned as JSON objects in the following format:
```json
{
    "success": false, 
    "error": 422,
    "message": "Request unprocessable"
}
```
The API will return these error types when requests fail:
- 400: Bad request
- 404: Resource not found
- 422: Request unprocessable

## Endpoints 

### GET /temperature

- Get temperature

- Example of response:
```json
{
  "data": 75,
  "success": true
}
```

### POST /temperature 

- Set a new temperature

- Example of response for a request with following body: `{ "temperature": 72 }` 

```json
{
  "data": 72,
  "success": true
}
```

### GET /lights 

- Get a list of all lights

- Example of response:

```json
{
  "data": [
        {
            "id": "83045cf9a3ba11eb9780d0abd5baaedb",
            "turnedOn": true
        },
        {
            "id": "4f98eb64a3e311eb88e4d0abd5baaedb",
            "turnedOn": false
        }
  ],
  "success": true
}
```

### POST /lights 

- Add a new light

- Example of response:

```json
{
  "data": {
        "id": "4f98eb64a3e311eb88e4d0abd5baaedb",
        "turnedOn": false
    },
  "success": true
}
```

### DELETE /lights/<light_id>

- Remove a light with the id:

- Example of response:

```json
{
  "light_deleted": "4f98eb64a3e311eb88e4d0abd5baaedb",
  "success": true
}
```

### GET /lights/<light_id>

- Get a light
- Example of response:

```json
{
  "data": {
        "id": "4f98eb64a3e311eb88e4d0abd5baaedb",
        "turnedOn": false
    },
  "success": true
}
```

### PUT /lights/<light_id>

- Turn on a light
- Example of response:

```json
{
  "data": {
        "id": "4f98eb64a3e311eb88e4d0abd5baaedb",
        "turnedOn": false
    },
  "success": true
}
```

## Tests

To run the tests locally, run `py test.py` from the `/backend` folder
