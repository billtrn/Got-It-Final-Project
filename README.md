# Got-It-Final-Project

Final Project for Got It Onboarding Program for Backend Intern. In this web application, users can create categories, post items to categories, and view others' items. This backend structure is created using RESTful APIs built with Python programming language, MySQL database, SQLAlchemy toolkit, and Flask microframework.

## Installation

#### 1. Install and activate virtual environment
Make sure that you already are in root directory of the project before running the following code.
```
$ pip install virtualenv                       
$ virtualenv venv --python=python3.8              
$ source venv/bin/activate             
```
	
#### 2. Install requirements
To install all the required libraries and packages for this project, run this command in your terminal:
```
pip install -r requirements.txt
```

#### 3. Setup database
Create 3 MySQL for 3 different environments for the project: development, production and test. 

After that, go to the corresponding config files, located at ~/FinalProject/configs and change the SQLALCHEMY_DATABASE_URI configuration based on this template:
```
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{username}:{password}@{host}:{port}/{database_name}'
For example: SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/final_project_dev'
```

#### 4. Change the configurations (optional)
Go to ~/FinalProject/configs/base.py and change the SECRET_KEY if you wish.

## Starting the server
In your terminal, run the following command:
```
$ python run.py
```


## Testing
In your terminal, run the following command:
```
$ ENVIRONMENT=test pytest --cov=main tests/
```
A detailed report will be returned.
