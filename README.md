README
----------
## Overview
[BtcImg](http://btcimg.com) is a Django web application that blurs an image upon upload, and progressively unblurs it as Bitcoin is sent to its address. Once 1 BTC has been sent to the address, the image is completely unblurred.


## Environment
1. Create a virtualenv called btcimg and install the python packages listed in requirements.txt. I recommend [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/command_ref.html) and will use that as an example:
    `mkvirtualenv btcimg`
    `workon btcimg`
    `git clone http://github.com/kvnn/btcimg`
    `cd btcimg`
    `pip install -r requirements.txt`

2. Create a settings/dev.py (see settings/dev_sample.py).

3. Optionally, create an .env file in the project root (or set BTCIMG_ENV_FILE variable to another file: logic in settings/__init__.py). This is where some required settings will be stored. See env_sample.


## Django stuff
1. python manage.py makemigrations
2. python manage.py migrate
3. python manage.py runserver

At this point, the Django server should be up and running locally. Please file an issue if you have problems.


## Author
Kevin Riggen |
[kriggen@gmail.com](http://mailto:kriggen@gmail.com) |
[kevinriggen.com](http://kevinriggen.com)