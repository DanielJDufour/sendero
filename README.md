# sendero
Data Filtering for Humans

## why sendero?
"sendero" means footpath in Spanish

## install
```bash
pip install sendero
```

## usage
```py
from sendero import list_paths

# list of cars with their previous owners
cars = [
  { "make": "Nissan", "model": "Altima", "year": 2022, "owners": [{ "id": 1, "name": "Juan" }, { "id": 2, "name": "Mark" }]},
  { "make": "Nissan", "model": "Kicks", "year": 2021, "owners": [{ "id": 3, "name": "Zach" }]},
  { "make": "Toyota", "model": "Camry", "year": 1995, "owners": [{ "id": 4, "name": "Tom" }]}
]
paths = list_paths(cars)
[
  "make",
  "model",
  "owners.id",
  "owners.name",
  "year"
]
```