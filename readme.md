# Harris County District Court Criminal Public Dataset Scraper
An API server that downloads the daily criminal disposition and criminal filing datasets from http://www.hcdistrictclerk.com/Common/e-services/PublicDatasets.aspx, parses the data, and adds the data into a database for further processing.

## Motivation
This project was started to support a module of the [Tubman Project](http://www.tubmanproject.com/).
A database of criminal filings and dispositions will provide the input data for machine learning applications that can predict the likelihood of upcharges in criminal cases or discover bias trends in court decisions.  

## Build status
Incomplete not working

## Technology and Frameworks Used
#### Built with
* [Flask: a mircoframework for Python](http://flask.pocoo.org/)
* [SQLite](https://www.sqlite.org/) *for development only*

## Installation
Clone this repository.
Navigate to the location on your system where you want to install this project and create a directory
```
$ mkdir myproject
$ cd myproject
$ git clone https://github.com/tyronemsaunders/hcdc_criminal_scraper.git .
```
*Note the dot at the end of the <b>git clone</b> command*


Install Virtualenv for isolated Python project environments.
Use the following command for Mac OS X or Linux.
```
$ sudo pip install virtualenv
```

Create a new Virtualenv for the Python project
```
$ virtualenv .venv
```

Activate the Virtualenv
```
$ . .venv/bin/activate
```
Notice the shell changed to show the active environment.

When necessary deactivate the Vitualenv with the command
```
$ deactivate
```

Install Flask and dependencies for this project.
Make sure you are in the root directory for this project. 
In the activated virtualenv run the following commands.
```
$ pip install -r requirements.txt
```

For a development workflow reference the [link](https://www.kennethreitz.org/essays/a-better-pip-workflow) for details on the commands below.
```
$ pip install -r requirements-to-freeze.txt --upgrade
$ pip freeze > requirements.txt
```

## API Reference
TBD

## How to use?
### Configuration
Edit the file at https://github.com/tyronemsaunders/hcdc_criminal_scraper/blob/master/app/config.py and add configuration details.

### Usage
Remember to work inside of the virtualenv shell
For development environments on Mac OSX or Linux set the FLASK_APP environment variable
```
$ export FLASK_APP=/path/to/project/run.py
```

Initialize and seed the database with the following command:
```
$ flask initdb
```

Run the application
```
$ flask run
```

The application should now be running on at localhost:5000.
Call the API endpoints described above i.e. `curl -X POST http://127.0.0.1:5000/api/scraper/disposition/today`

## Contribute
TBD

## Credits
Flask project layout and directory structure has been influenced by the [DoubleDibz](https://github.com/spchuang/DoubleDibz-tutorial/tree/master/FINAL) project created by [spchuang](https://github.com/spchuang)

## License

## TODO
* Handle file not found exceptions to prevent the rest of code from running
* Add criminal filings
* Abstract out defendants as a separate model
* Convert to Python > 3.5 and use asyncio
* Add database seeding with data from past dispositions and filings and field names