# FLASK REST API #
A simple todo CRUD REST API created using Flask and SQLAlchemy and tested with unittest.

## Instructions ##
Move (cd) into the project directory and type in command prompt.
### Create Virtual Environment and Run the App ###

#### Create a virtual environment ####
`py -m venv virt`

#### Activate the virtual environment ####
`.\virt\Scripts\activate`

#### Install required packages ####
`pip install -r requirements.txt`

#### Run the server ####
```
set FLASK_APP=api
set FLASK_ENV=development
flask run
```

#### Run tests ####
 `python -m unittest discover`

#### Check test coverage ####
```
coverage run -m unittest discover
coverage report
```
## Authorization Endpoints ##
* POST /api/sign-up
* GET /api/login

## User Endpoints ##
* GET /api/user                      
* GET /api/user/<public_id>	         
* PUT /api/user/<public_id>/promote  
* PUT /api/user/<public_id>/update	 	
* DELETE api/user/<public_id>        

## Todo endpoints ##
* POST /api/                         
* GET /api/todo                      
* GET /api/todo/<todo_id>            
* PUT /api/todo/<todo_id>           
* DELETE /api/todo/<todo_id>        

To run the API on Postman run the app and open http://127.0.0.1:5000 on Postman and make GET, POST, PUT, DELETE requests using the specified endpoints.\
To sign-up users use the format `{"name": <Username>, "password": <Password>}` inside the Postman body.\
To create todo items use the format `{"item": <Todo item description>}` inside the Postman body.