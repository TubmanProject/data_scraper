# Tubman Project API

The Tubman Project API is a REST-style web service that exposes endpoint's useful for interacting with the Tubman Project's data and services.  The primary audience for the API is developers that wish to build models and visualizations based on the data that powers the Tubman Project.

## Overview

The primary goal of the Tubman Project is to create a public defender AI; an open sourced tool that can be used by public defenders to help them defend their clients. This tool will be designed to take some of the load off of the public defenders who are often tasked with more cases than it is humanly possible to take on.

The Tubman Project API is designed to expose endpoints to data and project modules that will allow coders, activists, and lawyers to develop tools that address the challenges of the justice system.

### Technical Specs

The core software behind the Tubman Project API is [Python 3](https://www.python.org/).  This project was written using [Flask](http://flask.pocoo.org/), a Python micro-framework.

In addition to Python this project leverages [Celery](http://www.celeryproject.org/), an asynchronous task queue/job queue.

The Tubman Project API is backed by a [MongoDB](https://www.mongodb.com/) database.

The Tubman Project must be configured with the following software:

* [RabbitMQ](https://www.rabbitmq.com/) - Used as a message broker for Celery.
* [Redis](https://redis.io/) - Used for caching requests and as a results backend for Celery.
* [MongoDB](https://www.mongodb.com/) - Used as a database.

### Data

Data is the backbone of the Tubman Project API.  Our data is sourced from publicly available datasets offered by the courts of municipalities throughout the world.  This API is seeded with data from the [Harris County District Clerk public dataset](http://www.hcdistrictclerk.com/Common/e-services/PublicDatasets.aspx).

A great way to contribute to the project is to find a public dataset that can be scrapped and integrated into the Tubman Project API.

## Installation

We offer a [Chef repository](https://github.com/TubmanProject/chef-repo) as the recommended means for installing and getting started with the Tubman Project API.  With the Chef repository you can provision the API to either a virtual machine on your workstation or a remote server.

Instructions for manual installation are described below.

### Prerequisites

In order to install this project the following must be installed on your system:

* [Python 3.6+](https://www.python.org/downloads/)
* [pip](https://pypi.python.org/pypi/pip)
* [virtualenv](https://virtualenv.pypa.io/en/stable/)
* [RabbitMQ](https://www.rabbitmq.com/)
* [Redis](https://redis.io/)
* [MongoDB](https://www.mongodb.com/)

### General Installation

Clone this repository.
Navigate to the location on your system where you want to install this project and create a directory
```
$ mkdir myproject
$ cd myproject
$ git clone https://github.com/tubmanproject/tubmanproject_api .
```
**Note:** *The dot at the end of the <b>git clone</b> command which will clone this repository into the `myproject` directory*


Install `virtualenv` for isolated Python project environments.
Use the following command for Mac OS X or Linux.

```
$ sudo pip install virtualenv
```

Create a new `virtualenv` for the Python 3 project.

```
$ virtualenv .venv -p python3
```

Activate the `virtualenv`

```
$ . .venv/bin/activate
```

Notice the shell changed to show the active environment.

When necessary deactivate the `virtualenv` with the command:

```
$ deactivate
```

Install Flask and dependencies for this project.
Make sure you are in the root directory for this project.
In the activated `virtualenv` run the following commands.

```
$ pip3 install -r requirements.txt --upgrade
```

For a development workflow reference the [link](https://www.kennethreitz.org/essays/a-better-pip-workflow) for details on the commands below.
```
$ pip install -r requirements-to-freeze.txt --upgrade
$ pip freeze > requirements.txt
```

### Configuration

The Tubman Project API was designed to be installed with [Chef](https://www.chef.io/chef/). If Chef is not used for installation further configuration is required by updating the source files.  

In order to connect the Tubman Project API application to RabbitMQ, Redis, and MongoDB the [config.py](https://github.com/TubmanProject/tubmanproject_api/blob/master/app/config.py) file must be updated with configuration details for those applications.

Open `config.py` and delete the lines that read configuration files from the server.
```
# read the configuration files
with open(os.path.join(os.getenv('APP_SECRETS_PATH'), server_name, 'secrets.json'), 'r') as api_config:
    api_settings = json.load(api_config)

with open(os.path.join(os.getenv('MONGODB_SECRETS_PATH'), 'secrets.json'), 'r') as mongodb_config:
    mongodb_settings = json.load(mongodb_config)

with open(os.path.join(os.getenv('RABBITMQ_SECRETS_PATH'), 'secrets.json'), 'r') as rabbitmq_config:
    rabbitmq_settings = json.load(rabbitmq_config)

with open(os.path.join(os.getenv('REDIS_SECRETS_PATH'), 'secrets.json'), 'r') as redis_config:
    redis_settings = json.load(redis_config)

with open(os.path.join(os.getenv('REDIS_HAPROXY_SECRETS_PATH'), 'secrets.json'), 'r') as redis_haproxy_config:
    redis_haproxy = json.load(redis_haproxy_config)

with open(os.path.join(os.getenv('RABBITMQ_HAPROXY_SECRETS_PATH'), 'secrets.json'), 'r') as rabbitmq_haproxy_config:
    rabbitmq_haproxy = json.load(rabbitmq_haproxy_config)
```

In `config.py` find the following variables and update them to reflect your settings.
```
SECRET_KEY = api_settings['SECRET_KEY']
SERVER_NAME = api_settings['SERVER_NAME']
MONGO_HOST = mongodb_settings['HOST'] or 'localhost'
MONGO_PORT = mongodb_settings['PORT'] or 27017
MONGO_PEM_KEYFILE = mongodb_settings['PEMKeyFile']
MONGO_USER = [i for i in mongodb_settings['USERS'] if i['username'] == api_settings['HOSTNAME']][0]
MONGO_USERNAME = MONGO_USER['username']
MONGO_PASSWORD = MONGO_USER['password']
MONGO_DBNAME = MONGO_USER['database']
MONGO_ROLES = MONGO_USER['roles']
REDIS_HOST = redis_settings['MASTER']['HOST']
REDIS_PORT = redis_settings['MASTER']['PORT']
REDIS_PASSWORD = redis_settings['MASTER']['PASSWORD']
RABBITMQ_USERNAME = 'guest'
RABBITMQ_PASSWORD = 'guest'
RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = rabbitmq_haproxy['RABBITMQ_HAPROXY']['PORT']  # port 5772 if using haproxy
RABBITMQ_VHOST = api_settings['HOSTNAME']
RABBITMQ_BROKER_URLS = rabbitmq_settings[RABBITMQ_VHOST]['broker_urls']
UPLOADS_DEFAULT_DEST = '/var/uploads'
LOG_FOLDER = os.path.join('/var/log/', api_settings['SERVER_NAME'])
AWS_ACCESS_KEY_ID = aws_config.get('default', 'aws_access_key_id')
AWS_SECRET_ACCESS_KEY = aws_config.get('default', 'aws_secret_access_key')
AWS_DEFAULT_REGION = aws_config.get('default', 'region')
DOMAIN_NAME = api_settings['DOMAIN_NAME']
SSL_CERTFILE = api_settings['SSL_CERTFILE']
SSL_KEYFILE = api_settings['SSL_KEYFILE']
```

## Usage

API documentation is available at <https://tubmanproject-api.mintyross.com>

### Getting Started

For development environments set the FLASK_APP environment variable.

`$ export FLASK_APP=/PATH/TO/PROJECT/run.py`

Initialize the database with the following command:

`$ flask initdb`

Seed the database:

`$ flask scrape --type disposition`
`$ flask scrape --type filing`

Run the application:

`$ flask run`

The application should now be running on at `localhost:5000`.

Call the API endpoints described above i.e. `curl -X POST http://127.0.0.1:5000/v1/dispositions?limit=10`

### API Access

Requests begin with:

`http://localhost:5000/v1/`

Request must also have a [resource/endpoint](https://tubmanproject-api.mintyross.com/#getting-started)

`http://localhost:5000/v1/RESOURCE`

### Responses

Responses are in `json` format that typically resemble the following:

```
{
  "success": true,
  "message": "Query successful",
  "data": {
    "metadata": {
      "batch_size": 10000,
      "links": {
        "next": {
          "href": "/v1/dispositions?query=L3YxL2Rpc3Bvc2l0aW9ucz9ydW5kYXRlX21pbj0yMDE4LTAxLTAyJnJ1bmRhdGVfbWF4PTIwMTgtMDEtMjMmZGVmZW5kYW50X3JhY2U9YmxhY2smY3VycmVudF9vZmZlbnNlX2xldmVsX2RlZ3JlZT1mZWxvbnk=_1"
        },
        "self": {
          "href": "/v1/dispositions?query=L3YxL2Rpc3Bvc2l0aW9ucz9ydW5kYXRlX21pbj0yMDE4LTAxLTAyJnJ1bmRhdGVfbWF4PTIwMTgtMDEtMjMmZGVmZW5kYW50X3JhY2U9YmxhY2smY3VycmVudF9vZmZlbnNlX2xldmVsX2RlZ3JlZT1mZWxvbnk=_1"
        }
      },
      "next": "L3YxL2Rpc3Bvc2l0aW9ucz9ydW5kYXRlX21pbj0yMDE4LTAxLTAyJnJ1bmRhdGVfbWF4PTIwMTgtMDEtMjMmZGVmZW5kYW50X3JhY2U9YmxhY2smY3VycmVudF9vZmZlbnNlX2xldmVsX2RlZ3JlZT1mZWxvbnk=_1",
      "query": "L3YxL2Rpc3Bvc2l0aW9ucz9ydW5kYXRlX21pbj0yMDE4LTAxLTAyJnJ1bmRhdGVfbWF4PTIwMTgtMDEtMjMmZGVmZW5kYW50X3JhY2U9YmxhY2smY3VycmVudF9vZmZlbnNlX2xldmVsX2RlZ3JlZT1mZWxvbnk=_1",
      "total": 67
    },
    "results": [
      {
        ...
      }
    ]
  }
}
```

### Pagination

Large responses are paginated and the next page is provided in the response of the current page.

The link to the next page is found in the response at `data.metadata.links.next.href`

An example request to the next page in the data set is the following:

`http://localhost:5000/v1/dispositions?query=L3YxL2Rpc3Bvc2l0aW9ucz9ydW5kYXRlX21pbj0yMDE4LTAxLTAyJnJ1bmRhdGVfbWF4PTIwMTgtMDEtMjMmZGVmZW5kYW50X3JhY2U9YmxhY2smY3VycmVudF9vZmZlbnNlX2xldmVsX2RlZ3JlZT1mZWxvbnk=_2`

### Resources

The following resources are exposed through the API.

* [Dispositions](https://tubmanproject-api.mintyross.com/#dispositions)
* [Filings](https://tubmanproject-api.mintyross.com/#filings)
* [Fields](https://tubmanproject-api.mintyross.com/#fields)

## Contributing

The git branching model is influenced by this [article](http://nvie.com/posts/a-successful-git-branching-model/) <http://nvie.com/posts/a-successful-git-branching-model/>.

## Credits

Flask project layout and directory structure has been influenced by the [DoubleDibz](https://github.com/spchuang/DoubleDibz-tutorial/tree/master/FINAL) project created by [spchuang](https://github.com/spchuang)

## License

TBD
