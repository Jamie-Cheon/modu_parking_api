# parking_api

## Introduction 
- cloning modu parking api project 


## features
- GPS tracking<br>
: This technology allows to find the location of the car and determine the distance to the nearest parking lot.<br>

- Booking<br>
: This feature allows reserving a parking spot. The user can find a place that fits the budget and pre-pay it by points.<br>

- Price Comparison<br>
: This feature provides an opportunity to compare prices. So, it’s easy for users to find the cheapest place nearby.<br>

- Distance Comparison<br>
: This feature provides an opportunity to compare distance between user and parking lot. So, it’s easy for users to find the nearest place.<br>

- Bookmark location<br>
: This feature allows users to save the place on their bookmark. <br>


## models
- User
- Lot
- Parking
- BookMark

## requirments
Project is created with:
* python 3.8.2
* django 3.0.7
* djangorestframework 3.11.0
* haversine 2.2.0

## urls
- users

POST /users/ 
: user register

PUT /users/id 
: update user profile

GET /users/id 
: user detail

POST /users/login 
: user login

DELETE /users/logout 
: user logout

DELETE /users/deactivate
: delete user account

GET /bookmark/
: bookmark list

POST /bookmark/
: create bookmark

DELETE /bookmark/id
: delete bookmark

- lots

POST /lots/
: register lot

PUT /lots/id
: update lot info

GET /lots/id
: lot detail

GET /lots/map(action) 
: lot mapview

DELETE /lots/id 
: delete lot


- parkings (login required)

POST /parkings/ 
: create parking event

GET  /parkings/
: parking history

GET  /parkings/id
: parking details

PUT  /parkings/id/
: add parking time


## contributors
- Joyykim
- Jamie-Cheon
- taehyu
- bunnycast
