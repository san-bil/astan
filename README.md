Flask-Bootstrap
---

Is a skeleton of a "Large" Flask application with Twitter bootstrap integration.

Getting started
---

Clone the repo to your computer in the desired folder:

~~~ sh
$ git clone https://github.com/albertogg/flask-bootstrap.git
~~~

Use the requirements.txt to start dependencies in your virtualenv:

~~~ sh
$ pip install -r requirements.txt
~~~

Start the server:

~~~ sh
$ python runserver.py
~~~

Open the browser in localhost port 5000:

~~~
open http://localhost:5000

or

open http://localhost:5000/hello/<yourname>
~~~

Initialize db
---

Set the db parameters in the default_settings.py or in the production.cfg file and then go to the interactive python shell and run:

~~~
>>> from application import db
>>> db.create_all()
~~~

***note: You must first create the database in Postgresql***

Unit testing
---

Add unittests to the manage_tests.py file and then start running the tests:

~~~ sh
$ python runtests.py
~~~

Production.cfg
---

To activate the production configuration; export the variable:

~~~ sh
export PRODUCTION_SETTINGS=/path/to/production.cfg
~~~


Changelog
---
**v0.2 / 2012/12/28**
  * Add Unittests
  * License
  * Configuration files
  * index.html template

**v0.1 / 2012/12/22**
  * Create Flask-Bootstrap skeleton.
  * Add Twitter bootstrap 2.2.2 to project.
  * Add SQLAlchemy to default skeleton.

ToDo
---

* Add a better template.
* Add error pages.
* More...