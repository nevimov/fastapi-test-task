A small web-application to perform [URL shortening](https://en.wikipedia.org/wiki/URL_shortening).
It takes a long link (aka destination URL) like:
[https://www.reporterit.com/2018/11/29/spanish-man-builds-60-foot-spaceship-to-visit-planet-from-his-novels/]
and shortens this to a link like:
[https://shorturl.com/2QrLPgx] (auto-generated) or [https://shorturl.com/60ft-spaceship] (custom user URL).

When the link is created, clicks on it will be redirected (307 Temporary Redirect) to the destination URL.


# Setting up a development environment

If you're using [Docker](https://www.docker.com), then everything is very simple:

1) Build and start the containers:
```console
docker-compose up --detach
```

2) Open a bash instance in the 'web' service container:
```console
docker exec -it shorturl_web_1 bash
```

3) Initialize the developer environment:
```console
./prestart.sh
```
This command runs migrations and fills the database with initial data.

4) You're all set. Start the server using:
```console
make server
```
and open [0.0.0.0](http://0.0.0.0) in your browser.


# Test users

**ordinary user** (has ~300 precreated short URLs):
```
login:     user@example.com
password:  dummypass
```

**superuser**:
```
login:     admin@example.com
password:  dummypass
```


# Migrations

As during local development your app directory is mounted as a volume inside
the container, you can also run the migrations with `alembic` commands inside
the container and the migration code will be in your app directory (instead of
being only inside the container). So you can add it to your git repository.

Make sure you create a "revision" of your models and that you "upgrade" your
database with that revision every time you change them. As this is what will
update the tables in your database. Otherwise, your application will have
errors.

* Start an interactive session in the 'web' container:
  ```console
  docker-compose exec web bash
  ```

* If you created a new model in `./app/models/`, make sure to
  import it in `./app/db/base.py`. The module should import all the models
  used by Alembic.

* After changing a model (for example, adding a column), inside the container,
  create a revision using a command like:
  ```console
  alembic revision --autogenerate -m "Add column last_name to User model"
  ```

* After creating the revision, run the migration in the database (this is what
  will actually change the database):
  ```console
  alembic upgrade head
  ```
