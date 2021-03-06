# Open Data Quizz Builder

Web-site for constructing Open Data (OD) Quizzes.

OD Quizz is a quiz featuring tables with official goverment statistics pulled out from the Open Data portals designed to motivate citizens participation, awareness and transparancy.


Goals: 

(1) provide easy access to and further encorage discovery, exploration and utilization of the goverment statistical data;

(2) crowdsourcing OD annotations for question answering (QA) from tables.


Method: gamification: game-with-a-purpose providing support for semi-automated quiz construction.

## Requirements

* pyyacp:

git clone https://github.com/ODInfoBiz/pyyacp.git
git checkout tags/v1.0

to add to $PYTHONPATH: export PYTHONPATH=$PYTHONPATH:/home/svakulenko/pyyacp/
to check: echo $PYTHONPATH  

pip install:

* Flask

* Flask-OAuth

* Flask-SQLAlchemy

* python-dateutil

* structlog

* pip install git+git://github.com/sebneu/anycsv.git

* unicodecsv


* semantic-ui https://semantic-ui.com/introduction/getting-started.html



## Features

* Facebook authentication


## Deployment

* Set up Facebook app at developers.facebook.com

This field must be at most 32 characters long. means that you did not insert your credentials in settings.py

App Domains: localhost
Add Platform -> Website -> Site URL: http://localhost:5000/

* To init and/or clear the DB run restart_db.py

* Start web-app:

python quizz.py


## Acknowledgments

* Jürgen Umbrich, Sebastian Neumaier, Vadim Savenkov. Open Data Hackathon WU. 2017.

* Declarative widgets Polymer elements https://github.com/jupyter-widgets/declarativewidgets/tree/master/elements

* Armin Ronacher. PyLadies Flask Workshop tutorial. https://github.com/mitsuhiko/pyladies-flask

* HTML Quizz Tutorial https://css-tricks.com/building-a-simple-quiz/

## Inspiration and Related Work

* CSV Engine http://data.wu.ac.at/csvengine/clean

* Alan Smith. https://www.ted.com/talks/alan_smith_why_we_re_so_bad_at_statistics

* http://www.neighbourhood.statistics.gov.uk

* Gapminder. Global Ignorance Project. http://www.gapminder.org/ignorance/

* https://www.typeform.com/examples/quizzes/

* https://www.buzzfeed.com/quizzes
