*An
---

*An (pronounced AstAn) is a web-based tool for collecting video annotations.

~~~
Requirements
---
* Python
* sqlite
* pip
~~~
Getting started
---

Clone the repo to your computer in the desired folder:

~~~ sh
$ git clone https://github.com/san-bil/astan.git
~~~

Use the requirements.txt to install dependencies (try to use conda/virtualenv):

~~~ sh
$ apt-get install python-dev
$ conda create -n astan python=2.7
$ source activate astan
$ pip install -r requirements/astan_reqs.txt
~~~

Change default_settings.py to define defaults for:
* where to find taskdefs
* where to store data
* authentication details for AstAn's email.

Change runserver.py to define:
* what port to run on


Start the server:
~~~ sh
$ python runserver.py
~~~

Event Annotator (EvAn)
---
<img src="https://cloud.githubusercontent.com/assets/1110545/20281290/daf9406a-aaa7-11e6-8d9d-5e237e21a5e6.png" style="width:100; height:100"/>

Continuous Annotator (ConAn)
---
<img src="https://cloud.githubusercontent.com/assets/1110545/20281291/dafccbcc-aaa7-11e6-9b80-31e77e9caadc.png" style="width:100; height:100"/>
