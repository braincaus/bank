# Bank

This project was build as part of a Code Challenge.

In order to run it locally is important you have installed Python and Virtualenv or Similar to create python's 
virtual envs.

Once you are sure of the above, run on your terminal:

    python manage.py migrate
    python manage.py runserver

After that, you can open your browser on [http://localhost:8000/api/](http://localhost:8000/api/).

Where you will be able to use the API, however, if you wish it is also possible to consume it through the API Client of 
your choice.

A set of test were build, to run these:

    python manage.py test

The API schema (OpenAPI Documentation) is in the file named [openapi-schema.yml](openapi-schema.yml).

I have taken the liberty to make a second version taking into account some changes and scenarios that are not taken 
into account, to see these changes please switch to the **_V2_** branch.
