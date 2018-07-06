# carpoolling-ride-my-way 

[![Build Status](https://travis-ci.org/collinewait/carpoolling-ride-my-way.svg?branch=develop)](https://travis-ci.org/collinewait/carpoolling-ride-my-way)[![Coverage Status](https://coveralls.io/repos/github/collinewait/carpoolling-ride-my-way/badge.svg)](https://coveralls.io/github/collinewait/carpoolling-ride-my-way)[![Maintainability](https://api.codeclimate.com/v1/badges/acb8766d9fea3341890d/maintainability)](https://codeclimate.com/github/collinewait/carpoolling-ride-my-way/maintainability)

Ride-my App is a carpooling application that provides drivers with the ability to create ride offers  and passengers to join available ride offers.

**Features**

    - Register a user
    - Login a user 
    - Fetch all available rides 
    - Fetch the details of a single ride
    - Make a ride request
    - Create a ride offer 
    - Fetch all ride requests
**API end points**

- POST api/v1/auth/signup 
- POST api/v1/auth/login 
- GET api/v1/rides 
- GET api/v1/rides/#
- POST api/v1/rides/#/requests
- POST api/v1/users/rides
- GET api/v1/users/rides/#/requests

**Getting Started**

These instructions will enable you to run the project on your local machine.

**Prerequisites**

Below are the things you need to get the project up and running.

- git : To update and clone the repository
- python2.7 or python3: Language used to develop the api
- pip: A python package used to install project requirements specified in the requirements text file.

**Installing the project**

Type: 
        
        "git clone https://github.com/collinewait/carpoolling-ride-my-way.git"
   in the terminal or git bash or command prompt.

To install the requirements. run:

      pip install -r requirements.txt

cd to the folder carpoolling-ride-my-way
And from the root of the folder, type:
      
      python run.py
      
To run the tests and coverage, from the root folder, type: 
        
        pytest --cov=api/
