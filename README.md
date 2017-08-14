AnagramAPI
----------

This project showcases my vision on how the Anagram API server should be implemented.

The goals that were achieved:

* Adding a list of words to a database
* Computing the anagrams of the words and store them for retrieval
* Retrieve the words associated to an anagram, counts of palindromes, counts of anagrams, and counts of words
* Clear a word from our database & clear entire database

This is a personal project skeleton that I use for freelance work or personal projects.
I have taken parts that I agree with it's structure and setup which allow for modularity. This modularity enabled me to shift the app structure which fit the requirements given.

### Notes
I believe this produces a fairly performant system to compute anagrams. I'm using celery to handle all the large computing so users
wouldn't be negatively affected by a timeout or waiting for the server response. If there is a bottleneck, we could increase workers to evenly distribute work.
Celery allows for task chaining which is a fantastic feature that I used in my solution because I wanted to separate each task. 
This also allows us to use the save words functionality elsewhere. 

I originally attempted using Postgres to store information, however
there was a large time overhead to verify if words or anagrams are in the db. I settled on Redis because the key/value nature allowed for extremely quick 
inserts and lookup. The only drawback is that we use a lot more memory.

There are some flaws in this system. I am using [Walrus](https://github.com/coleifer/walrus/) which is a nice Redis wrapper and acts like an ORM. I chose this 
because I wanted to build a prototype quickly; if I had more time to build this then I would have queried Redis directly. Walrus doesn't update secondary indices correctly,
so if you delete a word it will not update the AnagramKey set nor the palindrome index which results in an error. I wrote a workaround which doesn't cause the server to crash,
it may have fixed that issue.

I would have also liked to split/refine the tasks a bit more and chunk the work so we could have multiple workers tackle the queue.

You can view the api endpoints at: http://127.0.0.1:8000/api/v1/

Installation
------------

## Docker
Easiest way to run this server is using Docker:

    $ docker-compose up --build

## Local
Running locally you need to have RabbitMQ and Redis running.

First create your virtual env first using Python 3.6.

Run the following commands:

    $ pip install --editable .
    $ app server dependencies
    $ app server run_celery
    $ app server run_server    

The first command will setup the CLI tool. The other commmands run the server.
    
    
Project Structure
-----------------

### Root folder

Folders:

* `app` - This RESTful API Server example implementation is here.
* `flask_restplus_patched` - There are some patches for Flask-RESTPlus (read
  more in *Patched Dependencies* section).
* `cli` - All the CLI commands are listed here. Type `app` in the project root to see all available commands.
* `tests` - These are [pytest](http://pytest.org) tests for this RESTful API
  Server example implementation.

### Application Structure

* `app/__init__.py` - The entrypoint to this Anagram API Server
  application which creates the app and celery as a factory.
* `app/extensions` - All extensions (e.g. SQLAlchemy, Redis, etc) are initialized
  here and can be used in the application by importing as, for example,
  `from app.extensions import db`.
* `app/modules` - All endpoints are expected to be implemented here in logicaly
  separated modules. It is up to you how to draw the line to separate concerns
  (I can create a monolith or microservices with this setup).
* `app/tasks.py` - All the celery tasks are located here.
  
Dependencies
------------

### Core Project Dependencies

* [**Python**](https://www.python.org/) 3.6
* [**Flask-Restplus**](https://github.com/noirbizarre/flask-restplus) (+
  [*flask*](http://flask.pocoo.org/))
* [**Marshmallow**](http://marshmallow.rtfd.org/) (+
  [*marshmallow-sqlalchemy*](http://marshmallow-sqlalchemy.rtfd.org/),
  [*flask-marshmallow*](http://flask-marshmallow.rtfd.org/)) - for
  schema definitions. (*supported by the patched Flask-RESTplus*)
* [**Walrus**](https://github.com/coleifer/walrus/) - for Redis ORM-like functionality
* [**Celery**](https://github.com/celery/celery) - for task processing

