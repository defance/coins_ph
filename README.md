Overview
========

This is home-test project for Coins.

This application is generic payment-system that support creation of transactions.

Provided API
============

[GET] /api/accounts/

    Return list of all existing accounts in the following format:

        [
            {
                "name": account_name,
                "currency": currency_code,
                "balance": current_account_balance
            }
        ]

[GET] /api/payments

    Return list of all performed payments in the following format:

        [
            {
                "id": payment_uuid,
                "from_account": account_name,
                "to_account": account_name,
                "amount": payment_amount,
                "currency": currency_code
            }
        ]

[POST] /api/payments/

    Attempts to create payment.

    Request body should be in json format. Example of request body:

        {
            "from_account": account_name,
            "to_account": account_name,
            "amount": payment_amount
        }

    The request will fail with corresponding message under following
    conditions:
        * Any of accounts (`from_account` or `to_account`) does not
          exist
        * Participants' currency are not the same (exchange is not
          supported)
        * Payment account exceeds source account's (`from_account`)
          balance

Deploy
======

Ensure that you have `docker` and `docker-compose` installed.
To run the app execute following commands:

    make build
    make start_db
    make configure
    make start
    make create_superuser
    
For details on the commands see `Usage` section.
During the first deploy (with empty database) see `First configuration` section.

First configuration
===================

The app comes with no sample data. You need to create manually neccessary objects in the Django admin.

1. Login with the user you created with `make create_superuser`.
2. Create one or several `Currency` objects. Codes are unique.
3. Create several users. Their names are unique. Balance and currency are also required.

After that you should be able to use the api from the `Provided API` section.


Usage
=====

The project comes with Makefile to easily manage builds and deploy. It supports following targets:

build
-----
Builds docker image with application and its dependencies.

start_db
--------
Starts database required for the systems using docker.

configure
---------
Configures app (performs migrations, collects static). It requires database being run. See `start_db`.

start
-----
Starts app and its requirements. Latter it will be available at localhost:8000

status
------
Shows status of the applications (simply shows docker-compose output).

logs
----
Shows and follows application logs including nginx and database.

test
----
Runs tests inside the docker container (not locally!)

create_superuser
----------------
Handy command to create superuser using current app. Latter one will be able to login into running app.
You will need the superuser to create sample users in the `/admin` section.


Local development
=================

The project uses pipenv to handle dependencies.

To run tests locally ensure that you have `pipenv` installed. Then execute:

    pipenv install
    pipenv shell
    python manage.py test

You may also want to run application locally. It uses sqlite for database. You will need to create superuser using
manage.py command. Also see `First configuration` to make app work.