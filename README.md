# urlshortener

## Usage

#### Start up the api
To start up the api and the database run the following command

`docker-compose up`

or

`docker-compose up -d`

to run in detached mode.

#### Access postgres shell (psql)
To access the postgres shell you need to get the id of the container

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

