Kushillu
========

Kushillu: Means "Monkey" in kichwa. This is a simple Continuous Integration based on Django and docker with excellent github integration.

Supports:
* **Build Badge** showing status (building, passing, failing) for use in readme files.
* **Github webhooks** to kick off builds
* **Github status updates** to mark commits and pull requests as passing/failing.
* **intelligent setup caching** for faster build. A persistent attached volume on the docker image allows you to check the hash of your pre test setup (eg. python's `requirements.txt` file) and copy it into place if it exists instead of rebuilding it.
* **prebuild/build** split, so you can visually and logically split CI setup and actual setup.
* **Coverage** the output can be parsed for the coverage value which which is then listed next to builds.

## Basic Setup

Run the following:

    cd /var/www/
    git clone git@github.com:codeadict/kushillu.git
    cd kushillu/
    virtualenv env
    source env/bin/activate
    pip install -r requirements.txt 
    grablib grablib.json
    ./manage.py syncdb

## To run the dev server

This assumes you have docker installed and working.

    ./manage.py runserver

## To deploy with Nginx

This assumes:
* you already have Nginx working 
* this repository is cloned to `/var/www/kushillu`
* the setup above is permformed (virtualenv, grablib, syncdb)
* docker is installed and setup to be usable by you web server user (www-data)

We're going to run kushillu as the `www-data` user, if you wish to use sqlite (you shouldn't) give `www-data` access to the project dir.

    sudo chown -R kushillu:www-data /var/www/kushillu

Edit one of the `setup/conf_nginx.conf ` to set your server

Copy it to `available-sites` and enable it

    sudo cp setup/conf_nginx.conf /etc/nginx/sites-available/kushillu.conf
    sudo ln -s /etc/nginx/sites-available/kushillu.conf /etc/nginx/sites-enabled/

Check the user id for `www-data`

    id -u www-data

set `uid` and `gid` to that value in `setup/uwsgi.ini`

Start `uwsgi`:

    sudo /var/www/kushillu/env/bin/uwsgi --ini /var/www/kushillu/setup/uwsgi.ini

You can check the log to see if it's started ok:

    sudo tail -n 100 /var/log/kushillu-uwsgi.log

If everything has gone ok you can restart nginx:

    sudo service nginx restart

You can make sure the system start after reboot by adding the following to `/etc/rc.local`:

    /var/www/kushillu/setup/start_uwsgi.sh
    
## Docker Setup

Follow [the docker instructions](https://docs.docker.com/) to install docker.

Make sure you can use docker without super user privileges **and that www-data can do the same**.

To enable www-data to use docker:

    sudo gpasswd -a www-data docker
    sudo service docker.io restart

Then "log in" www-data again, the easiest way is `sudo reboot`.

Kushillu needs a docker image to use for builds, by default this is called `kushillu` (can be changed on project setup) 
to create such an image from the example docker file `docker/Dockerfile` run

    docker build -t kushillu docker/Dockerfile

## localsettings.py and S3

You should overwrite some of the vital system settings in localsettings.py, but is not included in the repo for security reason.

This also allows you to configure kushillu to save code backups in S3.

    # to allow django to send you emails on system errors, examples uses gmail for convienience
    EMAIL_USE_TLS = True
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_HOST_USER = '<< username >>'
    EMAIL_HOST_PASSWORD = '<< password >>'
    
    DATABASES = {'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'kushillu',
        'USER': 'postgres',
        'PASSWORD': 'kushillu',
        'HOST': 'localhost',
        'PORT': '',
        'CONN_MAX_AGE': None
    }}
    
    SECRET_KEY = '!!! set a random string here !!!'
    
    ADMINS = (('<< your name >>', '<< your email address >>'),)
    MANAGERS = ADMINS
    
    # to use S3 for saving backups, use the following
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    AWS_QUERYSTRING_AUTH = True
    AWS_S3_SECURE_URLS = True
    AWS_DEFAULT_ACL = 'private'
    AWS_QUERYSTRING_EXPIRE = 600
    AWS_ACCESS_KEY_ID = 'aws access key'
    AWS_SECRET_ACCESS_KEY = 'aws secret key'
    AWS_STORAGE_BUCKET_NAME = 'aws bucket name'
    
    MEDIA_URL = 'https://s3.amazonaws.com/%s/' % AWS_STORAGE_BUCKET_NAME
