# Task API
Based in Python Flask.

## Introduction
Task rest API backend using MongoDB.

## Setup
Install project dependencies

````
python -m pip install -r .\requirements.txt
````

Create environment variables as follows

Windows
````
$env:application_root="/api/v1.0"
$env:mongodb_url="mongodb://<host>:<port>/"
$env:db_name="<database>"
$env:collection_name="<collection>"
````

## Run

````
python -m flask --app app run
````