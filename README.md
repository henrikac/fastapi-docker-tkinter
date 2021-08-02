# urlshortener

A url shortener.  

The purpose of this project is to learn about [FastAPI](https://fastapi.tiangolo.com/), [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/).

It turned out to a 2-in-1 project. It started as an API project but it ended up including a GUI made with [tkinter](https://docs.python.org/3/library/tkinter.html) that interacts with this API.  

## Requirements
+ Python 3.6+
+ Docker
+ Docker Compose

## Usage

#### Start up the api
To start up the api and the database run the following command

`docker-compose up`

or

`docker-compose up -d`

to run in detached mode.

#### Access postgres shell (psql)
To access the postgres shell you need to get the id of the postgres container

```terminal
$ docker ps
CONTAINER ID    IMAGE              ...
b563764171e2    urlshortener_api   ...
c6e480b0f26a    postgres           ...
```

Now run 

```terminal
$ docker exec -it <container id> sh

# su - postgres

$ psql
```

#### Run the GUI
To run the GUI simply run `python3 gui/gui/main.py`.

