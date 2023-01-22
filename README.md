# Bank

This project was build as part of a Code Challenge, with some small changes to make the exercise more similar to what 
really happens. For which "Celery" was added for queue management.

In order to run it locally is important you have installed Python and Virtualenv or Similar to create python's 
virtual envs.

A `.env` file must be created with:

    SECRET_KEY='django-insecure-&nt1^sx(=$*o=n&ml#ke--8b4x19n^_2u437(s_*fc3&xcuss2'
    DEBUG=True
    RABBITMQ_HOST=localhost
    RABBITMQ_USER=bank
    RABBITMQ_PASSWORD=bank
    RABBITMQ_VHOST=bank

Once you are sure of the above, run on your terminal:

    python manage.py migrate
    python manage.py runserver

In order to run the worker locally, a docker-compose with a RabbitMQ service.

    docker-compose up -d                                 # To up service
    celery -A bank.celery worker --loglevel=info         # To up worker

After that, you can open your browser on [http://localhost:8000/api/](http://localhost:8000/api/).

Where you will be able to use the API, however, if you wish it is also possible to consume it through the API Client of 
your choice.

A set of test were build, to run these:

    python manage.py test

The API schema (OpenAPI Documentation) is in the file named [openapi-schema.yml](openapi-schema.yml).

I have taken the liberty to make a second version taking into account some changes and scenarios that are not taken 
into account, to see these changes please switch to the **_V2_** branch.
